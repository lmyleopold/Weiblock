import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import requests
import re
import json
import sys
from lxml import etree
import csv
import logging
from collections import Counter
from datetime import datetime, timedelta

weibo_1file = "../data/weibo.csv"


def url_parse(url):
    """Parse url of a single weibo into uid and wid(62base mid)"""
    l = re.search(r"(?<=weibo\.com)/(\d+)/([a-zA-Z\d]+)/?",url)
    if l is None:
        logging.warning("Invalid weibo url: {}".format(url))
        return None
    uid = l.group(1)
    wid = l.group(2)
    return uid, wid


def url_gen(**kwargs):
    if 'wid' in kwargs:
        return 'https://weibo.com/ajax/statuses/show?id={}'.format(kwargs['wid'])
    elif 'uid' in kwargs:
        if 'page' in kwargs:
            url = 'https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0'.format(kwargs['uid'], kwargs['page'])
        else:
            url = 'https://weibo.com/ajax/profile/detail?uid={}'.format(kwargs['uid'])
        return url


def wid2mid(wid):
    """Decode 62 based wid to mid"""
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    wid_slices = [wid[0:-8], wid[-8:-4], wid[-4:]]
    res = ""
    for s in wid_slices:
        num = 0
        for index, char in enumerate(s[::-1]):
            num += BASE62.index(char) * (62 ** index)
        res += "{0:07}".format(num)
    res = int(res)
    return res


def mid2wid(wid):
    """Decode 62 based wid to mid"""
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    wid = str(wid)
    wid_slices = [wid[0:-14], wid[-14:-7], wid[-7:]]
    res = None
    for s in wid_slices:
        num = int(s)
        s_res = ""
        while num:
            s_res = BASE62[num % 62] + s_res
            num = num // 62
        res = s_res if res is None else res + "{0:0>4}".format(s_res)
    return res


class CookiePool(object):

    def __init__(self, cookie_list):
        self.__good_list = cookie_list
        self.__last_cookie = None

    def get_cookie(self):
        self.__last_cookie = self.__good_list.pop()
        return self.__last_cookie

    def have_cookie(self):
        return True if self.__good_list else False


def time_convert(time):
    now = datetime.now()
    if re.match(".+年\d*月\d*日", time):
        time = datetime.strptime(time, "%Y年%m月%d日%H:%M")
        time = time.replace(year=now.year)
        return time
    elif re.match(".+月*日", time):
        time = datetime.strptime(time, "%m月%d日%H:%M")
        time = time.replace(year=now.year)
        return time
    elif re.match(".+分钟前", time):
        min = re.search("^(.+?)分钟前", time)
        min = min.group(1)
        min = timedelta(minutes=int(min))
        delta = now - min
        return delta
    elif re.match(".+秒前", time):
        second = re.search("^(.+?)秒前", time)
        second = second.group(1)
        second = timedelta(seconds=int(second))
        delta = now - second
        return delta
    elif re.match("今天*", time):
        time = time.replace("今天", "{0:02d}月{0:02d}日".format(now.month, now.day))
        time = datetime.strptime(time, "%m月%d日%H:%M")
        time = time.replace(year=now.year)
        return time
    else:
        logging.log(logging.WARNING, "Unknown time format: {}".format(time))
        return time


class WeiboRequest(object):

    def __init__(self, cookie_list, max_try = 3):
        self.__cookie_pool = CookiePool(cookie_list)
        self.__cookie = self.__cookie_pool.get_cookie()
        self.__header = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': self.__cookie,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'
        }
        self.__max_try = max_try

    def get_res(self, url, fn=None):
        res = None
        while True:
            for _ in range(self.__max_try):
                try:
                    res = requests.get(url, headers=self.__header, timeout=5)
                except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                    logging.warning(e)
                    logging.warning('           ~~~try ' + str(_) + ' times again~~~            ')
                else:
                    logging.info('Retrived: {}'.format(url))
                    break
            if not fn:
                break
            if fn(res):
                break
            if not self.__cookie_pool.have_cookie():
                raise ValueError("All cookie invalid")
            logging.warning("Cookie {} invalid".format(self.__cookie[:20]))
            self.new_cookie()
        return res

    def new_cookie(self):
        self.__cookie = self.__cookie_pool.get_cookie()
        self.__header['cookie'] = self.__cookie


class WeiboMessage(object):

    def __init__(self, wrequest, mid=None, url=None, message=None, fuzzy_message=None):
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

    def get_message(self):
        if self.message is None:
            r = self.wrequest.get_res(self.url, fn=lambda s: json.loads(s.text)['ok'] == 1)
            self.message = json.loads(r.text)
            self.message['time'] = datetime.strftime("")
        return self.message

    def get_basics(self):
        if self.message is None:
            self.get_message()
        m = self.message
        return {'wid': m['id'], 'created_at': datetime.strptime(m['created_at'], '%a %b %d %H:%M:%S %z %Y'), 'reposts_count': m['reposts_count'],
                'comments_count': m['comments_count'],
                'attitudes_count': m['attitudes_count'], 'uid': m['user']['id'], 'text_raw': m['text_raw']}


class WeiboUser(object):

    def __init__(self, wrequest, uid):
        self.uid = uid
        self.wrequest = wrequest
        self.user = None
        self.user_messages = []

    def __hash__(self):
        return self.uid

    def __str__(self):
        return "{}:{}".format(self.user['id'], self.user['screen_name'])

    def get_detail(self):
        if self.user is None:
            r = self.wrequest.get_res(url_gen(uid=self.uid), fn=lambda s: json.loads(s.text)['ok'] == 1)
            self.user = json.loads(r.text)
        return self.user

    def get_messages(self):
        if not self.user_messages:
            r = self.wrequest.get_res(url_gen(uid=self.uid, page=1), fn=lambda s: json.loads(s.text)['ok'] == 1)
            self.user_messages = json.loads(r.text)
        self.user_messages = [WeiboMessage(self.wrequest, message=x) for x in self.user_messages['data']['list']]
        return self.user_messages

    def get_basics(self):
        profile = self.user['data']['user']
        return [self.uid, profile['screen_name'], profile['followers_count'], profile['friends_count'], profile['location'],
                profile['verified_reason'], profile['description']]


def get_keyword(key_word, wrequest, page):

    messages = []
    for i in range(1, page + 1):
        res_topic = wrequest.get_res(
            'https://s.weibo.com/weibo?q=' + key_word + '&Refer=SWeibo_box&page=' + str(i),
            lambda x: not re.match(r"^.*login.*", x.url))
        # print(res_topic.text)
        bs_topic = BeautifulSoup(res_topic.text, 'html.parser')

        messages_html = bs_topic.find_all('div', class_='card')
        for message_html in messages_html:
            message = {}
            # 获取 发表时间 和 信息(有设备和转发点赞数，但是并不是每一条都有)
            metadata_html = message_html.find('p', class_='from')
            try:
                url = metadata_html.a.attrs['href']
            except AttributeError:
                continue

            message['user'] = {}
            message['user']['id'], message['id'] = url_parse(url)
            info = metadata_html.text.replace('\n', '').replace(' ', '').encode("GBK", 'ignore').decode("GBK")
            time = re.search(r".+分钟前|.+秒前|.+月.+日\d{2}:\d{2}|今天\d{2}:\d{2}", info)
            message['time'] = time_convert(time.group(0))

            content_html = message_html.find('p', class_='txt')     # 本人的发言
            message['user']['screen_name'] = content_html['nick-name']
            message['text_raw'] = content_html.text.replace('\n', '').replace(' ', '').encode("GBK", 'ignore').decode("GBK")

            bottom_html = message_html.find('div', class_='card-act')
            feedback_html = bottom_html.find_all('a')

            try:
                message['reposts_count'] = int(feedback_html[0].get_text().replace(' ', ''))
            except ValueError:  # 0 repost will not be displayed in text attribute
                message['reposts_count'] = 0
            try:
                message['comments_count'] = int(feedback_html[1].get_text().replace(' ', ''))
            except ValueError:
                message['comments_count'] = 0
            try:
                message['attitude_count'] = int(feedback_html[2].get_text().replace(' ', ''))
            except ValueError:
                message['attitude_count'] = 0
            messages.append(WeiboMessage(wrequest, mid=wid2mid(message['id']), fuzzy_message=message))
            # try:
            #     print(messages[-1])
            # except KeyError:
            #     print(messages[-1].message)
    return messages


def get_topic(key_word, wrequests, page=10):
    return get_keyword("%23"+key_word+"%23", wrequests, page)


def split_messages(messages):
    messages.sort()
    messages_group = [[messages[0]]]
    delta = timedelta(days=1)
    for i in range(len(messages) - 1):
        if messages[i + 1].message['time'] - messages[i].message['time'] > delta:
            messages_group.append([messages[i + 1]])
        else:
            messages_group[-1].append(messages[i + 1])
    return messages_group


def search_source(messages):
    source = []
    for s in split_messages(messages):
        source.append(s[0])
    return source


def heat(messages, segments=100):
    messages.sort()
    span = max((messages[-1].message['time'] - messages[0].message['time']) / (segments + 1), timedelta(seconds=1))
    heat_time = []
    i = 0
    while i < len(messages):
        start = i
        heat_time.append([messages[i].message['time'], 0])
        while i < len(messages) and messages[i].message['time'] - messages[start].message['time'] < span:
            heat_time[-1][-1] += messages[i].message['reposts_count'] \
                                + messages[i].message['attitude_count'] * 0.2 \
                                + messages[i].message['comments_count'] * 0.5 + 1
            i += 1
    return heat_time


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    cookies = [
        "SINAGLOBAL=250399977033.21326.1642248696644; ULV=1652717505324:13:3:1:7899870900341.525.1652717505269:1652526857382; ALF=1685558426; UOR=,,login.sina.com.cn; MEIQIA_TRACK_ID=28pBqsAxXYW9T1VuX7gUBCQsbfK; MEIQIA_VISIT_ID=28pBqqiSwzIM1RsiyG0Hhm0YJ0b; SCF=Apklbmk7BN5fhN4Q4A5I1owknOzYRMweleWTI3C6YjhEbkfQcJiXfEzeyGLe9A_dp-1FBfrY68Z4zK8rXLOnIMg.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5NSkNLqgONq9X2AFplTF2U5JpX5KMhUgL.Fo-pe0nRSh5XeKz2dJLoI7DjIHvRIg44qg4r; SUB=_2A25PkhFLDeRhGeNP6FoZ9C7Iyj6IHXVs5gWDrDV8PUNbmtAKLVHRkW9NSbWLCU2jtFxrbjYJyiBF9_NKUJAmV-rr; SSOLoginState=1654022427; XSRF-TOKEN=re5vV8BiT3LyHCWcAb7_aJ5y; WBPSESS=2bh1_9aErW2ebTbocgVd3Bx7lTQmOCX0h7oqRUyVpqF11sR8vlhznoMLlYSQWeTF6iZGRGrRTRQRCihMTUI-zZgsYGglox_YeF56K2Oyk1MqEtpLsljRHomUGq02JtHx24vOZ1cAaCQrp_jVrJbkfg=="
    ]
    wrequest = WeiboRequest(cookies, 3)
    messages = get_keyword("上海疫情部分工作人员失职", wrequest, page=20)
    src = search_source(messages)
    with open("../data/weibo.csv", "w") as f:
        csv.writer(f)
        f.writelines([str(m) + '\n' for m in src])
    with open("../data/heat.csv", "w") as f:
        csv.writer(f)
        for group in split_messages(messages):
            f.writelines(['{},{}\n'.format(h[0], h[1]) for h in heat(group)])
            f.write('---------\n')
