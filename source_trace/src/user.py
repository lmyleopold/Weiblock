# -*- coding:utf-8 -*-
# @time: 2021/5/20 5:20
# @Author: 韩国麦当劳
# @Environment: Python 3.7
# @file: 有情人终成眷属.py
import requests
import csv
import time
import json


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://weibo.com"
    }
    cookies = {
        "cookie": "SINAGLOBAL=4405234143066.801.1645179232587; UOR=,,www.baidu.com; SSOLoginState=1647618833; wvr=6; wb_view_log_7510888322=1440*9601.5; webim_unReadCount={'time':1647619420001,'dm_pub_total':1,'chat_group_client':0,'chat_group_notice':0,'allcountNum':33,'msgbox':0}; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFBGVqcLMrcoNAEH-EQHMEL5JpX5KMhUgL.FoMfeK5R1hn0eoz2dJLoI7YLxKqLBozLBK8ixhM71hMt; SRT=D.QqHBJZPAOPPNR!Mb4cYGS4SJicoHd8sDRbBuPDSHNEYdVsHwNsMpMERt4EPKRcsrA8sJPOiMTsVuObEnPEi8MQBaVGPZJbzrQsYjNmEFiebQT3P8JZSnOFb!*B.vAflW-P9Rc0lR-ykVDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWFA!WdVdiJOQHZUruBM4XkMPEzO4PJi49ndDPIOdYPSrnlMcyiScPIiPzoTFtnSdywJcM1OFyHisbJ5mkoOmH65!oCNqY95FYiiqEfOQA7; SRF=1647653899; ALF=1679189898; SCF=AkGp5WgN7QUSWQeGADxbvs-wR0E48JhYzi0uwefpCi9nO0gi_GsYEeDuUcJsTJd0vWemFIOQjASbmD9Ycnr1xYk.; SUB=_2A25PMURbDeRhGeFL6lIZ-CbPyT6IHXVsRzKTrDV8PUNbmtANLW_DkW9NQpTSbA3rir-wiCuN5y1drdgL7CYN5okq; XSRF-TOKEN=R7-zueHzWXtnYxd0kAE-Su3Q; _s_tentry=weibo.com; Apache=6898857975603.534.1647653912483; ULV=1647653912595:4:3:3:6898857975603.534.1647653912483:1647618634520; WBPSESS=Dt2hbAUaXfkVprjyrAZT_H2ebbLtCPwePrXKPqZc_1_ZmoJSlNSiRdU9DZu7kaum-Ozc4S8krqYBEQXPLsB2U87dKwGjD2-jMJ4DMcSKfHJXc5wcR0zD0V55okg8VsnmzYyNM0xb6T02va8uNfoJvbN6tC0J1twPL2261_wEDy0FNX8ljXmgU_PoQnqaL5sD9lUTXyJfb8mePisht8wsag=="
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(3)   # 加上3s 的延时防止被反爬
    return response.text


def save_data(data):
    title = ['text_raw', 'created_at', 'attitudes_count', 'comments_count', 'reposts_count']
    with open("data.csv", "a", encoding="utf-8", newline="")as fi:
        fi = csv.writer(fi)
        fi.writerow([data[i] for i in title])


if __name__ == '__main__':
    page = 1
    uid = 3108949955
    url = 'https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0'
    sinceid = 0
    print(page)
    url = url.format(uid, page)
    print("正在爬取的url:", url)
    html = get_html(url)
    responses = json.loads(html)
    blogs = responses['data']['list']
    # print(responses)
    sinceid = responses['data']['since_id']
    # print("siceid:",sinceid)

    data = {}  # 新建个字典用来存数据
    for blog in blogs:
        data['attitudes_count'] = blog['attitudes_count']  # 点赞数量
        data['comments_count'] = blog['comments_count']  # 评论数量(超过100万的只会显示100万)
        data['created_at'] = blog['created_at']  # 发布时间
        data['reposts_count'] = blog['reposts_count']  # 转发数量(超过100万的只会显示100万)
        data['text_raw'] = blog['text_raw']  # 博文正文文字数据
        save_data(data)
    page += 1

    while 1:
        print(page)
        url = 'https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0&since_id={}'
        url = url.format(uid, page, sinceid)
        print("正在爬取的url:",url)
        html = get_html(url)
        responses = json.loads(html)
        blogs = responses['data']['list']
        # print(responses)
        sinceid = responses['data']['since_id']
        # print("siceid:",sinceid)
        if len(blogs) == 0:
            break
        # data = {}  # 新建个字典用来存数据
        for blog in blogs:
            data['attitudes_count'] = blog['attitudes_count']   # 点赞数量
            data['comments_count'] = blog['comments_count']     # 评论数量(超过100万的只会显示100万)
            data['created_at'] = blog['created_at']     # 发布时间
            data['reposts_count'] = blog['reposts_count']     # 转发数量(超过100万的只会显示100万)
            data['text_raw'] = blog['text_raw']     # 博文正文文字数据
            save_data(data)
        page += 1
