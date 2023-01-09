import json
import logging

from utils import url_gen
from weibo import WeiboMessage
from connector import save

"""
A weibo user contains following fields:
id: User id of the user
screen_name: Username of the user

-- Optional --
followers_count: Number of followers
following_count: Number of following users
plist: List of weibo posts
ip_location: 
followers_list: a (partial) list of followers
"""


class WeiboUser(object):

    def __init__(self, wrequest, uid, user=None):
        self.uid = uid
        self.wrequest = wrequest
        self.user = user if user else None
        self.messages = []

    def __hash__(self):
        return self.uid

    def __str__(self):
        return "{}:{}".format(self.user['id'], self.user['screen_name'])

    @staticmethod
    def rewrite(user: dict) -> dict:
        """
        Rewrite some of the key in response json user from weibo
        """
        user['following_count'] = user['friends_count']
        return user

    def get_user(self):
        if self.user is None:
            r = self.wrequest.get_res(url_gen(uid=self.uid))
            self.user = json.loads(r.text)['data']['user']
            self.user = self.rewrite(self.user)
        return self.user

    def get_messages(self):
        if not self.messages:
            r = self.wrequest.get_res(url_gen(uid=self.uid, page=1))
            self.messages = json.loads(r.text)
        self.messages = [WeiboMessage(self.wrequest, message=x) for x in self.messages['data']['list']]
        return self.messages

    def get_basics(self):
        if self.user is None:
            self.get_user()
        profile = self.user['data']['user']
        return [self.uid, profile['screen_name'], profile['followers_count'], profile['friends_count'], profile['location'],
                profile['verified_reason'], profile['description']]

    def save(self) -> None:
        reduced_user_info = {
            'id': self.uid
        }
        u = self.user
        if not u:
            save('user', reduced_user_info)
            return
        optional_keys = ['screen_name', 'followers_count', 'following_count', 'plist', 'ip_location', 'followers_list']
        for key in optional_keys:
            try:
                reduced_user_info[key] = u[key]
            except KeyError:
                logging.log(logging.INFO, "Missing {} in user {}".format(key, self.uid))
        save('user', reduced_user_info)
