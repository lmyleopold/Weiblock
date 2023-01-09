import re
from typing import Optional
from bs4 import BeautifulSoup

from utils import url_parse, time_convert, wid2mid
from weibo import WeiboMessage
from user import WeiboUser
from connector import walk_collection


def get_keyword(keyword, wrequest, end_page, save: bool = False, repost_pages: Optional[int] = None, start_page: int = 1):

    print("Keyword: {}".format(keyword))
    messages = []
    for i in range(start_page, end_page + 1):
        print("Getting page {}".format(i))
        res_topic = wrequest.get_res(
            'https://s.weibo.com/weibo?q=' + keyword + '&Refer=SWeibo_box&page=' + str(i),
            lambda x: not re.match(r"^.*login.*", x.url))
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

            uid, wid = url_parse(url)
            message['uid'] = int(uid)
            message['id'] = wid2mid(wid)
            info = metadata_html.text.replace('\n', '').replace(' ', '').encode("GBK", 'ignore').decode("GBK")
            time = re.search(r".+分钟前|.+秒前|.+月.+日\d{2}:\d{2}|今天\d{2}:\d{2}", info)
            message['time'] = time_convert(time.group(0))

            content_html = message_html.find('p', class_='txt')     # 本人的发言
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
                message['attitudes_count'] = int(feedback_html[2].get_text().replace(' ', ''))
            except ValueError:
                message['attitudes_count'] = 0
            message = WeiboMessage(wrequest, mid=message['id'], fuzzy_message=message)
            if repost_pages:
                message.get_reposts(pages=repost_pages)
            if save:
                message.save()
                user = WeiboUser(wrequest, uid=uid)
                # user.get_user()
                user.save()

            messages.append(message)

            print("Retrieved: {}".format(url))

            # try:
            #     print(messages[-1])
            # except KeyError:
            #     print(messages[-1].message)
            # Retrive user
    return messages


def add_reposts(wrequest, depth: int, repost_pages: int = 1):
    for _ in range(depth):
        for weibo in walk_collection('weibo'):
            print(weibo)
            try:
                for repost_id in weibo['rlist']:
                    print(repost_id)
                    repost = WeiboMessage(wrequest, mid=repost_id)
                    repost.get_reposts(pages=repost_pages)
                    repost.save()
            except KeyError:
                pass
