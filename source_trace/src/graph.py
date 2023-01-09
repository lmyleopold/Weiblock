import csv
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from collections import Counter

def parse_time(time):
    now = datetime.now()
    try:
        ret = datetime.strptime(time, "%m月%d日%H:%M")
        ret = ret.replace(year=now.year)
    except ValueError:
        ret = datetime.strptime(time, "%Y年%m月%d日%H:%M")
    return ret


if __name__ == "__main__":
    weibo_list = []
    with open('../data/weibo.csv', newline='') as f:
        weibo_reader = csv.reader(f)
        for rows in weibo_reader:
            weibo_list.append( (parse_time(rows[2]), rows[0]) )
    # print(*weibo_list, sep="\n")

    # plot timeline
    splited_weibo_list = []
    hour_count = Counter()
    for i in range(1, len(weibo_list)):
        if weibo_list[i-1][0] - timedelta(days=2) > weibo_list[i][0]:
            break
        splited_weibo_list.append(weibo_list[i])
        hour_index = datetime(year=weibo_list[i][0].year,
                              month=weibo_list[i][0].month,
                              day=weibo_list[i][0].day,
                              hour=weibo_list[i][0].hour)
        hour_count[hour_index] += 1
    # print(splited_weibo_list[-1])
    hour_count = [(key, value) for key, value in hour_count.most_common()]
    print(hour_count)
    plt.bar(*zip(*hour_count))
    plt.show()

    # find newest weibo
