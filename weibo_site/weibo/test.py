# import re
#
# with open(r'weibo/templates/weibo/pic.html', 'r') as file:
#     data = file.read()
# data = data.replace('\n', '')
# data = re.findall('<body>(.*?)</body>', data)[0]
# with open(r'weibo/templates/weibo/pic.txt', 'w+') as file:
#     file.write(data)
import os, csv, re
import time

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
comments = {}
with open(PROJECT_ROOT + r'/weibo/weibo.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    for each in reader:
        if len(each) > 1:
            each[0] = each[0].split(':')[0]
            try:
                comments[each[0]].append([each[1],each[2]])
            except:
                comments[each[0]] = [[each[1],each[2]]]

print(comments)
