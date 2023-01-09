import re
import logging
from datetime import datetime, timedelta


def url_parse(url: str) -> (int, str):
    """Parse url of a single weibo into uid and wid(62base mid)"""
    l = re.search(r"(?<=weibo\.com)/(\d+)/([a-zA-Z\d]+)/?",url)
    if l is None:
        logging.warning("Invalid weibo url: {}".format(url))
        return None
    uid = int(l.group(1))
    wid = l.group(2)
    return uid, wid


def url_gen(**kwargs) -> str:
    if 'wid' in kwargs:
        if 'rlist' in kwargs:
            return 'https://weibo.com/ajax/statuses/repostTimeline?id={}&page={}&moduleID=feed&count=10'.format(kwargs['wid'], kwargs['page'])
        else:
            return 'https://weibo.com/ajax/statuses/show?id={}'.format(kwargs['wid'])
    elif 'uid' in kwargs:
        if 'page' in kwargs:
            url = 'https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0'.format(kwargs['uid'], kwargs['page'])
        else:
            url = 'https://weibo.com/ajax/profile/info?uid={}'.format(kwargs['uid'])
        return url


BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def wid2mid(wid: str) -> int:
    """Decode 62 based wid to mid"""
    wid_slices = [wid[0:-8], wid[-8:-4], wid[-4:]]
    res = ""
    for s in wid_slices:
        num = 0
        for index, char in enumerate(s[::-1]):
            num += BASE62.index(char) * (62 ** index)
        res += "{0:07}".format(num)
    res = int(res)
    return res


def mid2wid(mid: int) -> str:
    """Decode 62 based mid to wid"""
    mid = str(mid)
    wid_slices = [mid[0:-14], mid[-14:-7], mid[-7:]]
    res = None
    for s in wid_slices:
        num = int(s)
        s_res = ""
        while num:
            s_res = BASE62[num % 62] + s_res
            num = num // 62
        res = s_res if res is None else res + "{0:0>4}".format(s_res)
    return res


def time_convert(time) -> datetime:
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
