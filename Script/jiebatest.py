# -*- coding: utf-8 -*-
__author__ = 'tornado'
import jieba

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))


# from django.shortcuts import render
#
# # Create your views here.
# from django.http import HttpResponse
# import jieba
# import json
#
#
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
#
#
# def fenci(request):
#     content = request.GET.get('content')
#     seg_list = jieba.cut(content)
#     strdata = ".".join(seg_list)
#     array = strdata.split('.')
#     data = [{'status': 1, 'dict': array}]
#     return HttpResponse("Full Mode: " + json.dumps(data))