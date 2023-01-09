import requests
import logging
import json
from time import sleep
from json import JSONDecodeError
from typing import Optional, Callable

from cookie import CookiePool


def check_ok(r: requests.Response):
    try:
        return json.loads(r.text)['ok'] == 1
    except JSONDecodeError:
        return False


class WeiboRequest(object):

    def __init__(self, cookie_list, max_try=3):
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

    def get_res(self, url, fn: Optional[Callable[[requests.Response], bool]] = check_ok):
        """
        :param url:
        :param fn: fn is used to check if response is valid
        """
        res = None
        while True:
            for _ in range(self.__max_try):
                try:
                    res = requests.get(url, headers=self.__header, timeout=5)
                except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                    logging.warning(e)
                    logging.warning('           ~~~try ' + str(_) + ' times again~~~            ')
                else:
                    if fn(res):
                        logging.info('Retrieved: {}'.format(url))
                        sleep(0.3)
                        return res
                sleep(1)
            if not self.__cookie_pool.have_cookie():
                raise ValueError("All cookie invalid")
            logging.warning("Cookie {} invalid".format(self.__cookie[:20]))

    def new_cookie(self):
        self.__cookie = self.__cookie_pool.get_cookie()
        self.__header['cookie'] = self.__cookie