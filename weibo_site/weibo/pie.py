import plotly.offline as py
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import requests
import re
import json
import time
import os
import csv


def draw_pie(labels, values):
    # py.init_notebook_mode(connected=True)

    trace = [
        go.Pie(
            labels=labels,
            values=values,
            # hole=0.7,
            hoverinfo='label+percent',  # hoverinfo属性用于控制当用户将鼠标指针放到环形图上时，显示的内容
            # pull=[0.1, 0, 0, 0, 0],  # 弹出效果
            textfont=dict(size=60)
        )
    ]
    layout = go.Layout(
        # title='情感分析图',
        # titlefont=dict(size=40),
        showlegend=True,
        legend=dict(
            x=0.7,
            y=1,
            font=dict(size=40)
        ),

    )

    fig = go.Figure(data=trace, layout=layout)
    fig.write_html('templates/weibo\\' + 'pic.html')
    py.plot(fig)
    # with open(r'weibo/templates/weibo/pic.html', 'r') as file:
    #     data = file.read()
    # data = data.replace('\n', '')
    # data = re.findall('<body>(.*?)</body>', data)[0]
    # with open(r'weibo/templates/weibo/pic.txt', 'w+') as file:
    #     file.write(data)


def get_pie_html():
    data = []
    with open(r'weibo/emotion.csv', 'r', encoding='gbk') as file:
        reader = csv.reader(file)
        next(reader)
        for each in enumerate(reader):
            data.append(each[1])

    num = [{'value': 0, 'name': 'positive'}, {'value': 0, 'name': 'negative'}, {'value': 0, 'name': 'mid'}]
    headers = ['positive', 'negative', 'mid']
    for each in data:
        if each[9] == 'positive':
            num[0]['value'] += 1
        elif each[9] == 'negative':
            num[2]['value'] += 1
        else:
            num[1]['value'] += 1

    return headers, num
    # draw_pie(headers, num)
# get_pie_html()
