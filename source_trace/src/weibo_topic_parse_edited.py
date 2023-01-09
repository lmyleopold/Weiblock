import pandas as pd
import time
from bs4 import BeautifulSoup
# from selenium import webdriver
import requests
import re
from lxml import etree
import csv

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

def save_info(list_l):
    """保存用户在该话题下的发言等内容"""
    file = open("weibo_topic_2.csv", "a", newline="")
    csv_write = csv.writer(file)
    csv_write.writerow(list_l)
    file.close()

def get_likes(key_word='每天啥都不想干怎么办', page=10,
              cookie='SINAGLOBAL=2098324754978.6355.1605005382608; _s_tentry=-; Apache=7998144335383.353.1647506010591; ULV=1647506010902:4:1:1:7998144335383.353.1647506010591:1632023171386; WBtopGlobal_register_version=2022031721; appkey=; SSOLoginState=1647590897; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWWEleRxboxC_bQ4lyPibg5JpX5KMhUgL.FoME1KzpeoBfSK22dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeo.EeKzXSK-p; ALF=1679280507; SCF=Agzk46qA_eMUhM5YMn03I7LzK5jcIa36kZTzcuvjZtawR5VYDdHB1Z7f9gQoeoDIU2bIlCZWMP_rXTluP56a5ig.; SUB=_2A25PMuWtDeRhGeFM4lAQ8irJzj2IHXVsRlBlrDV8PUNbmtB-LXHFkW9NQIgfYDk4RoRkdZdhfCfmEZBCJNfN0y9v; UOR=www.52jingsai.com,widget.weibo.com,login.sina.com.cn; WBStorage=f4f1148c|undefined; webim_unReadCount=%7B%22time%22%3A1647744696923%2C%22dm_pub_total%22%3A6%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A46%2C%22msgbox%22%3A0%7D'
              ):
    save_info(['收藏','转发','评论','点赞'])
    for i in range(1, page):
        res_topic = get_res(
            'https://s.weibo.com/weibo?q=%23' + key_word + '%23&Refer=SWeibo_box&page=' + str(i), cookie)
        # print(res_topic.text)
        bs_topic = BeautifulSoup(res_topic.text,'html.parser')
        # print(bs_topic)
        list_likes = bs_topic.find_all('div',class_='card-act')
        # print(list_likes)
        # list_all = []
        for likes in list_likes:
            tag_a = likes.find_all('a')
            list_l = []
            j = 1
            for tag in tag_a:
                if tag == None:
                    list_l.append('无')
                else:
                    l = tag.text.replace('\n','').replace(' ','').encode("GBK", 'ignore').decode("GBK")
                    if j == 4: 
                        if l == '':
                            list_l.append('0')
                        else:
                            list_l.append(l)
                    else:
                        if l[2:] == '':
                            list_l.append('0')
                        else:
                            list_l.append(l[2:])
                j+=1
            # list_all.append(list_l)
            save_info(list_l)
    # print(list_all)

def save_text(time,rest,name,content,emoji):
    # """保存用户在该话题下的发言等内容"""
    file = open("weibo_topic_1.csv", "a", newline="")
    csv_write = csv.writer(file)
    csv_write.writerow([time,rest,name,content,emoji])
    file.close()

def get_topic(key_word='每天啥都不想干怎么办', page=10,
              cookie='SINAGLOBAL=2098324754978.6355.1605005382608; _s_tentry=-; Apache=7998144335383.353.1647506010591; ULV=1647506010902:4:1:1:7998144335383.353.1647506010591:1632023171386; WBtopGlobal_register_version=2022031721; appkey=; SSOLoginState=1647590897; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWWEleRxboxC_bQ4lyPibg5JpX5KMhUgL.FoME1KzpeoBfSK22dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeo.EeKzXSK-p; ALF=1679280507; SCF=Agzk46qA_eMUhM5YMn03I7LzK5jcIa36kZTzcuvjZtawR5VYDdHB1Z7f9gQoeoDIU2bIlCZWMP_rXTluP56a5ig.; SUB=_2A25PMuWtDeRhGeFM4lAQ8irJzj2IHXVsRlBlrDV8PUNbmtB-LXHFkW9NQIgfYDk4RoRkdZdhfCfmEZBCJNfN0y9v; UOR=www.52jingsai.com,widget.weibo.com,login.sina.com.cn; WBStorage=f4f1148c|undefined; webim_unReadCount=%7B%22time%22%3A1647744696923%2C%22dm_pub_total%22%3A6%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A46%2C%22msgbox%22%3A0%7D'
              ):
    save_text('发表时间','信息','用户名','内容','用到表情')
    for i in range(1, page):
        res_topic = get_res(
            'https://s.weibo.com/weibo?q=%23' + key_word + '%23&Refer=SWeibo_box&page=' + str(i), cookie)
        # print(res_topic.text)
        bs_topic = BeautifulSoup(res_topic.text,'html.parser')
        
        list_topic = bs_topic.find_all('div',class_='content')
        
        list_all = []
        for topic in list_topic:

            # 获取 发表时间 和 信息(有设备和转发点赞数，但是并不是每一条都有)
            tag_p = topic.find('p',class_='from')
            if(tag_p is None):
                continue
            info = tag_p.text.replace('\n','').replace(' ','').encode("GBK", 'ignore').decode("GBK")
            time = info[0:11]
            rest = info[11:]

            # 获取 用户名 和 内容
            # 如果有引用 ———— 被引用内容、用户和时间
            '''if topic.find('div',class_='card-comment') != None:
                tag_div = topic.find('div',class_='card-comment')
                tag_p = tag_div.find('p',class_='txt')
                tag_p_full = tag_div.find(attrs={'node-type':'feed_list_content_full'}) # 某些长内容需要展开获取
                if tag_p_full != None:
                    content_quote = tag_p_full.text.replace('\n','').replace(' ','').encode("GBK", 'ignore').decode("GBK")
                else:
                    content_quote = tag_p.text.replace('\n','').replace(' ','').encode("GBK", 'ignore').decode("GBK")
                tag_p = tag_div.find('p',class_='from')
                time_quote = tag_p.text.replace('\n','').replace(' ','').encode("GBK", 'ignore').decode("GBK")
                tag_a = tag_div.find('a',class_='name')
                info_quote = tag_a['nick-name'] # 获取被引用用户名
                name_quote = info_quote[0:11]
                rest_quote = info_quote[11:]
                tag_img = tag_div.find_all('img',class_='face')
                emoji_quote = []
                for tag in tag_img:
                    emoji_quote.append(tag['title'])
                list_all.append([time_quote,rest_quote,name_quote,content_quote,emoji_quote])
                save_text(time_quote,rest_quote,name_quote,content_quote,emoji_quote)'''

            # 本人的发言
            tag_p = topic.find('p',class_='txt')
            name = tag_p['nick-name']
            content = tag_p.text.replace('\n','').replace(' ','').encode("GBK", 'ignore').decode("GBK")
            # print(content)
            if content[-5:] == "展开全文c":
                tag_p = topic.find(attrs={'node-type':'feed_list_content_full'})
                content = tag_p.text.replace('\n','').replace(' ','').encode("GBK", 'ignore').decode("GBK")

            tag_img = tag_p.find_all('img',class_='face')
            emoji = []
            for tag in tag_img:
                emoji.append(tag['title'])
            list_all.append([time,rest,name,content,emoji])
            save_text(time,rest,name,content,emoji)
        # print(list_all)

get_topic()
get_likes()

f1 = pd.read_csv('weibo_topic_1.csv',encoding='gbk')
f2 = pd.read_csv('weibo_topic_2.csv',encoding='gbk')
file = [f1,f2]
train = pd.concat(file,axis=1)
train.to_csv("weibo_topic" + ".csv", index=0, sep=',')

