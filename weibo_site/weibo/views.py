import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .pie import get_pie_html
import re
import os, csv

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))


def index(request):
    # with open('weibo/templates/weibo/pic.txt', 'r') as file:
    #     chart_pie = file.read()
    header, num = get_pie_html()
    header = json.dumps(header)
    num = json.dumps(num)
    points = [[0, 1], [1, 2], [3, 1]]
    with open(PROJECT_ROOT + r'/weibo/templates/weibo/css/weibo_site.css', 'r', encoding='utf-8') as file:
        css = file.read()
    # with open(PROJECT_ROOT + r'/weibo/templates/weibo/js/echarts.min.js', 'r', encoding='utf-8') as file:
    #     js = file.read()

    return render(request, 'weibo/index.html', locals())

@login_required
def china(request):
    points = [[0, 1], [1, 2], [3, 1]]
    with open(PROJECT_ROOT + r'/weibo/templates/weibo/css/weibo_site.css', 'r', encoding='utf-8') as file:
        css = file.read()
    return render(request, 'weibo/china.html', locals())


@login_required
def points(request):
    ids = []
    with open(PROJECT_ROOT + r'/weibo/each_round_infected.csv') as file:
        reader = csv.reader(file)
        for each in reader:
            ids.append(each)
    points = []
    with open(PROJECT_ROOT + r'/weibo/all_id_list.csv') as file:
        reader = csv.reader(file)
        for each in reader:
            points.append(each)
    relations = []
    with open(PROJECT_ROOT + r'/weibo/weibo_forward_list_uid.csv') as file:
        reader = csv.reader(file)
        reader.__next__()
        for each in reader:
            relations.append(each)
    with open(PROJECT_ROOT + r'/weibo/templates/weibo/css/weibo_site.css', 'r', encoding='utf-8') as file:
        css = file.read()
    return render(request, 'weibo/points.html', locals())


@login_required
def timeline(request):
    points = []
    with open(PROJECT_ROOT + r'/weibo/timeline.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for each in reader:
            points.append(each)
    heat = []
    with open(PROJECT_ROOT + r'/weibo/heat.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for each in reader:
            if len(each) > 1:
                heat.append(each)
    comments = []
    with open(PROJECT_ROOT + r'/weibo/weibo.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        # for each in reader:
        #     if len(each) > 1:
        #         each[0] = each[0].split(':')[0]
        #         try:
        #             comments[each[0]].append([each[1],each[2]])
        #         except:
        #             comments[each[0]] = [[each[1],each[2]]]
        for each in reader:
            comments.append(each)
    with open(PROJECT_ROOT + r'/weibo/templates/weibo/css/weibo_site.css', 'r', encoding='utf-8') as file:
        css = file.read()
    return render(request, 'weibo/timeline.html', locals())
