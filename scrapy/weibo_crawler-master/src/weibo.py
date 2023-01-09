import json
import logging
from datetime import datetime

from utils import url_parse, url_gen, wid2mid, mid2wid
from connector import save, in_collection
from weibo_requests import WeiboRequest

"""
A weibo message contains following fields:
id: A 12 digit integer. mid of a weibo message, e.g. 4799159913941994
uid: Integer, user id of author
url: url to this weibo
time: Time the message is posted
text_raw: Content of the post
reposts_count: Number of reposts (Maybe? containing repost of reposts)
comments_count: Number of comments
attitudes_count: Number of likes

-- Optional --
region_name: A string of approximate location. E.g "发布于 北京"
original_id: If the post is reposted, represent mid of the original post.
rlist: A list containing mid of reposts of this weibo message. Only fetched after calling get_reposts
hashtag: a list of hashtags
"""


class WeiboMessage(object):

    def __init__(self, wrequest: WeiboRequest, mid=None, url=None, message=None, fuzzy_message=None):
        """
        Use mid, url or message to initialize weibo message.
        Optionally, give a fuzzy_message to put off ajax request.
        """
        self.message = None
        if fuzzy_message is not None:
            self.message = fuzzy_message
        if url:
            uid, wid = url_parse(url)
            self.mid = wid2mid(wid)
            self.url = url_gen(wid=wid)
        elif mid:
            self.mid = mid
            self.url = url_gen(wid=mid2wid(mid))
        elif message:
            self.message = message
            self.mid = message['id']
            self.url = url_gen(wid=mid2wid(self.mid))
        else:
            raise ValueError("Neither mid, url nor message is given, failed to initialize")
        self.wrequest = wrequest

    def __hash__(self):
        return self.mid

    def __str__(self):
        return "{},{},{}".format(self.message['time'], self.message['id'], self.message['text_raw'])

    def __gt__(self, b):
        try:
            return self.message['time'] > b.message['time']
        except IndexError:
            logging.log(logging.ERROR, "Compared before getting weibo message")
            return None

    @staticmethod
    def rewrite(message):
        message['time'] = message['created_at']
        message['original_id'] = message['retweeted_status']['id']
        message['uid'] = message['user']['id']
        try:
            message['hashtag'] = message['tag_struct']
        except KeyError:
            pass
        return message

    def valid(self) -> bool:
        """
        TODO:
        Check if all the required arguments are in message json
        """
        pass

    def get_message(self) -> dict:
        if self.message is not None:
            return self.message
        elif m := in_collection('weibo', self.mid):
            self.message = m
            return {}
        else:
            r = self.wrequest.get_res(self.url)
            r_text = json.loads(r.text)
            self.message = r_text
            self.message = self.rewrite(self.message)
            return self.message

    def get_reposts(self, pages: int) -> None:
        if self.message is None:
            if self.get_message() == {}:
                return
        rlist = []
        page = 1
        max_page = 1

        while page <= max_page and page <= pages:
            url = url_gen(wid=mid2wid(self.mid), rlist=True, page=page)
            r = self.wrequest.get_res(url)
            r_text = json.loads(r.text)
            new_list = list(map(lambda x: x['id'], r_text['data']))   # Only need id of the reposts
            rlist += new_list
            page += 1
            max_page = r_text['max_page']

        if rlist:
            self.message['rlist'] = rlist

    def get_basics(self):
        if self.message is None:
            self.get_message()
        m = self.message
        return {'wid': m['id'], 'created_at': datetime.strptime(m['created_at'], '%a %b %d %H:%M:%S %z %Y'),
                'reposts_count': m['reposts_count'],
                'comments_count': m['comments_count'],
                'attitudes_count': m['attitudes_count'], 'uid': m['user']['id'], 'text_raw': m['text_raw']}

    def save(self) -> None:
        m = self.get_message() if not self.message else self.message
        reduced_message = {
            '_id': m['id'],
            'uid': m['uid'],
            'url': self.url,
            'time': m['time'],
            'text_raw': m['text_raw'],
            'reposts_count': m['reposts_count'],
            'comments_count': m['comments_count'],
            'attitudes_count': m['attitudes_count']
        }
        optional_keys = ['regine_name', 'original_id', 'rlist', 'hashtag']
        for key in optional_keys:
            try:
                reduced_message[key] = m[key]
            except KeyError:
                logging.log(logging.INFO, "Missing {} in message {}".format(key, self.mid))
        save("weibo", reduced_message)
