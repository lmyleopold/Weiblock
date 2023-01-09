import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup
# from selenium import webdriver
import requests
import re
from lxml import etree
import csv

user_flag = []
# user_flag = [0 for i in range(1111111111,10000000000)]
# user_flag = {}

def save_text(father_id, user_id):
    file = open("weibo_forward3.csv", "a", newline="")
    csv_write = csv.writer(file)
    csv_write.writerow([father_id, user_id])
    file.close()

def get_res(url, cookie):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie,
        'referer': 'https://s.weibo.com/weibo?q=%23%E6%AF%8F%E5%A4%A9%E5%95%A5%E9%83%BD%E4%B8%8D%E6%83%B3%E5%B9%B2%E6%80%8E%E4%B9%88%E5%8A%9E%23',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 QIHU 360SE',
    }
    print(url)
    i = 0
    while 1:
        try:
            i += 1
            time.sleep(1)
            res = requests.get(url, headers=headers, timeout=(21, 60))
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(e)
            print('           ~~~try ' + str(i) + ' times again~~~            ')
            if i > 3:
                return None
        else:
            print('success')
            return res
    # return None

blog_cnt = 0

def get_forward_url(id, father_id, depth, cookie):

    if depth == 0:      # 递归出口
        return

    father_id_1 = father_id

    forward_url = 'https://weibo.com/ajax/statuses/repostTimeline?id='+str(id)+'&page=0&moduleID=feed&count=10'
    res3 = get_res(forward_url, cookie)
    json_res3 = res3.json()
    page_count = json_res3['max_page']      # 通过json_res3['max_page']找到该博文下转发者的页数（动态页面）
    print(page_count)
    print(type(page_count))
    if page_count == None:
        return
    if page_count > 20:     # 对于几万转发的，先爬取前20页
        page_count = 20
    print(page_count)

    for i in range(page_count):     # 爬取转发者信息
        forward_url = 'https://weibo.com/ajax/statuses/repostTimeline?id='+str(id)+'&page='+str(i)+'&moduleID=feed&count=10'
        res3 = get_res(forward_url, cookie)
        json_res3 = res3.json()
        for each in json_res3['data']:
            if each['user']['id'] in user_flag:
                save_text(father_id, each['user']['id'])
                continue
            save_text(father_id, each['user']['id'])      # 一对父子节点
            user_flag.append(each['user']['id'])
            # print(each['user']['id'])
            # if depth < 5:
            #     print("--------------------------------------------------")
            # else:
            #     print("==================================================")
            
            forwarder_url = 'https://weibo.com/ajax/profile/myhot?page=1'+'&feature=2&uid='+str(each['user']['id'])     #来到该子节点的精选页搜索过往博文
            id_1 = each['user']['id']
            res4 = get_res(forwarder_url, cookie)
            json_res4 = res4.json()
            json_res4_data = json_res4['data']
            for each in json_res4_data['list']:
                # print(each['mblogid'])
                print(each['user']['id'])
                print("***********************************")
                if each['user']['id'] != id_1:      # 如果转发id和该子节点的id不一致，说明是快转微博，由于不存在对快转微博的再次转发，所以直接跳过即可
                    continue

                id = each['mblogid']
                father_id = each['user']['id']
                get_forward_url(id, father_id, depth-1, cookie)

            father_id = father_id_1
            

def get_forward(key_word='那些被疫情偷走的时光', page=10, depth=5,
              cookie='SINAGLOBAL=3817660732868.9194.1646569886063; PC_TOKEN=0d5993cc91; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWWEleRxboxC_bQ4lyPibg5JpX5KMhUgL.FoME1KzpeoBfSK22dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeo.EeKzXSK-p; ALF=1682394268; SSOLoginState=1650858269; SCF=Ag5fwbZEfeK5PKTrW-6FIRMn0a5iBm3w7caCmEtEUKeopFQKEX8GrMueEIS1OXIluFNB2KKcU0EEzStuEZXNRSk.; SUB=_2A25PYmlNDeRhGeFM4lAQ8irJzj2IHXVsFt2FrDV8PUNbmtANLVj_kW9NQIgfYH-Kh6uFZS_K8umxxNp-_af-wpz2; XSRF-TOKEN=vgxxAw5Tiyrk6yXvR_r_UdIW; _s_tentry=weibo.com; Apache=4877188332378.874.1650858317152; ULV=1650858317272:6:5:1:4877188332378.874.1650858317152:1650616357511; WBPSESS=PBXGHDtHOAmBEBjtDMiBlWDRiUad5Jik7jJpXuUF6H_1_9_jqXXVbsS7USu2TPVQYw2vXc4ePTHzqqHY0JU-RtXY3lBpDQvxaVPz5pU9lihvGTM9Bm_ht_XAlt8w5_qUVsZDua7L4rE_V_haqvkm_g=='
              ):
    save_text('father_id','user_id')
    for i in range(1, page):
        res_topic = get_res(
            'https://s.weibo.com/weibo?q=%23' + key_word + '%23&Refer=SWeibo_box&page=' + str(i), cookie)
        bs_topic = BeautifulSoup(res_topic.text,'html.parser')
        
        list_topic = bs_topic.find_all('p',class_='from')

        for topic in list_topic: # 对于该话题下每一条博文

            tag_a = topic.find('a')
            url = tag_a['href']
            # print(type(url))
            forward_list = url.split('?')
            fl = forward_list[0].split('/')

            res2 = get_res('https://weibo.com/ajax/statuses/show?id='+fl[4], cookie)
            # bs_res2 = BeautifulSoup(res2.text,'html.parser')
            json_res2 = res2.json()
            id = json_res2['id']         # id是该博文生成的一个id
            father_id = json_res2['user']['id']      # json_res2['user']['id']即当前这条博文博主的微博id号
            # print(father_id)
            get_forward_url(id, father_id, depth, cookie)   # 爬取该博文下的转发者


get_forward()
