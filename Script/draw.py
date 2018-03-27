# -*- coding: utf-8 -*-
__author__ = 'tornado'

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

plt.rcParams['axes.unicode_minus'] = False


def pie(data, img_name):
    # data = {
    # '南京' : (60, '#7199cf')
    # '上海' : (45, '#4fc4aa')
    # '北京' : (120, '#ffff10')
    # }

    # 设置绘图对象的大小
    fig = plt.figure(figsize=(8, 8))

    cities = data.keys()
    values = [x for x in data.values()]

    ax1 = fig.add_subplot(111)
    ax1.set_title('饼图')
    labels = ['{}:{}'.format(city, value) for city, value in zip(cities, values)]

    # 设置饼图的凸出显示
    explode = [0, 0.1]

    # 画饼状图, 并且指定标签和对应颜色
    # 指定阴影效果
    ax1.pie(values, labels=labels, explode=explode, shadow=True)

    plt.savefig('%s.png' % img_name)

    plt.show()

def bar(data, img_name):
    # data = {
    # '南京' : (60, '#7199cf')
    # '上海' : (45, '#4fc4aa')
    # '北京' : (120, '#ffff10')
    # }
    _keys, _values = zip(*sorted(data.items(), key=lambda t: t[1]))

    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)


    ind = np.arange(len(data))  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence

    #p1 = plt.bar(ind, menMeans, width, color='#d62728', yerr=menStd)
    #p2 = plt.bar(ind, womenMeans, width, bottom=menMeans, yerr=womenStd)

    p1 = plt.bar(ind, _values, width, color='#d62728')
    # X轴名称
    plt.ylabel('店铺数量')
    # 表格名称
    plt.title(img_name)
    # x轴参数
    plt.xticks(ind, _keys)
    # y轴比例 （起始，终点，刻度）
    plt.yticks(np.arange(0, _values[-1], 10))

    # 右上角标签
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    plt.savefig('%s.png' % img_name)

    plt.show()