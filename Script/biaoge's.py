#!/usr/bin/env python
# -*- coding:utf-8 -*-
from matplotlib import pyplot as plt
from datetime import datetime
import csv
filename = 'test.csv'
with open(filename) as f:
    # csv.reader是一个阅读器，类似文件一直处于阅读状态
    reader = csv.reader(f)
    header_row = next(reader)
    # enumerate函数是用来获取列表的索引和值,下面打印文件头索引和值
    for index, column_header in enumerate(header_row):
        print(index, column_header)

    # 初始化最高温度 最低温度  日期 列表
    TemperMax, TemperMin, date = [], [], []
    for row in reader:
        # 此处有时候会存在字段缺失的情况，这个时候，可以使用Try-except-else来避免程序直接异常
        try:
            # 因为图形插件识别的是int 类型的，读取之后是字符串，所以要先转换，记得，在上面的For循环转换
            current_data = datetime.strptime(row[0], "%Y-%m-%d")
            Temper_Max = int(row[2])
            Temper_Min = int(row[3])
            print("数据是:", current_data)
        except ValueError:
            print(current_data, '当天数据缺失')
        else:
            # 将获取的温度和日期存入列表
            date.append(current_data)
            TemperMax.append(Temper_Max)
            TemperMin.append(Temper_Min)
print(date)
fig = plt.figure(dpi=128, figsize=(10, 6))

# 需要画几条线时，设置几个plot方法即可，参数alpha的作用是指定线条的透明度，默认值是1,0表示透明
plt.plot(date, TemperMax, c='red', linewidth=1, alpha=0.5)
plt.plot(date, TemperMin, c='blue', linewidth=1, alpha=0.5)

# 下面的方法将使用方法fill_between(),接收一个X参数和两个参数，并填充两个Y系之间的空间
plt.fill_between(date, TemperMin, TemperMax, facecolor='green', alpha=0.1)

# 设置图形的格式
plt.title('Temp', fontsize=24)
plt.xlabel('', fontsize=6)
# 绘制倾斜的日期标签
fig.autofmt_xdate()
plt.ylabel('Temp', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()
