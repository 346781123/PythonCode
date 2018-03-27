# -*- coding: utf-8 -*-

import requests
import re
import json
import time
import xlwt
from Script import draw

key_word = input('请输出查询关键词: ')
DATA = []
G_COOKIE = ""
# url
old_url = "https://s.taobao.com/search?q=%s&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306" % (key_word)

api_url = "https://s.taobao.com/api?_ksTS=1521816927159_208&callback=jsonp209&ajax=true&m=customized&sourceId=tb.index&q=%s&spm=a21bo.2017.201856-taobao-item.1&s=36&imgfile=&initiative_id=tbindexz_20170306&bcoffset=0&commend=all&ie=utf8&rn=bb362c5ed7398ec527333c8b8ab74be9&ssid=s5-e&search_type=item" % (key_word)


#print(data_list)
def get_html_data(url,cookie=None):
    # 发送http请求
    response = requests.get(url,cookies=cookie)
    G_COOKIE = response.cookies
    # 分析找出信息
    html = response.text
    content = re.findall(r'g_page_config =(.*?)g_srp_loadCss', html, re.S)[0].strip()[:-1]
    # 格式化json
    content = json.loads(content)
    # 解析数据
    data_list = content['mods']['itemlist']['data']['auctions']
    for item in data_list:
        temp = {
            'title': item['title'],
            'view_price': item['view_price'],
            'view_sales': item['view_sales'],
            'view_fee': '否' if float(item['view_fee']) else '是',
            'isTmall': '是' if item['shopcard']['isTmall'] else '否',
            'area': item['item_loc'],
            'name': item['nick'],
            'detail_url': item['detail_url'],
        }
        DATA.append(temp)

def get_html_data_from_api(url,cookie=None):
    # 发送http请求
    response = requests.get(url,cookies=cookie)
    G_COOKIE = response.cookies
    # 分析找出信息
    html = response.text
    content = re.findall(r'{.*}', html, re.S)[0]
    # 格式化json
    content = json.loads(content)
    # 解析数据
    data_list = content['API.CustomizedApi']['itemlist']['auctions']
    for item in data_list:
        temp = {
            'title': item['title'],
            'view_price': item['view_price'],
            'view_sales': item['view_sales'],
            'view_fee': '否' if float(item['view_fee']) else '是',
            'isTmall': '是' if item['shopcard']['isTmall'] else '否',
            'area': item['item_loc'],
            'name': item['nick'],
            'detail_url': item['detail_url'],
        }
        DATA.append(temp)

def get_html_data_from_jsonp(url,cookie=None):
    # 发送http请求
    response = requests.get(url,cookies=cookie)
    G_COOKIE = response.cookies
    # 分析找出信息
    html = response.text
    content = re.findall(r'{.*}', html, re.S)[0]
    # 格式化json
    content = json.loads(content)
    # 解析数据
    data_list = content['mods']['itemlist']['data']['auctions']
    for item in data_list:
        temp = {
            'title': item['title'],
            'view_price': item['view_price'],
            'view_sales': item['view_sales'],
            'view_fee': '否' if float(item['view_fee']) else '是',
            'isTmall': '是' if item['shopcard']['isTmall'] else '否',
            'area': item['item_loc'],
            'name': item['nick'],
            'detail_url': item['detail_url'],
        }
        DATA.append(temp)
get_html_data(old_url)

get_html_data_from_api(api_url,G_COOKIE)



# 翻页
for i in range(1, 3):
    ksts = time.time()
    _ksTS = '%s_%s' % (int(ksts*1000),str(ksts)[-3:])
    callback = "jsonp%s" % (int(str(ksts)[-3:]) + 1)
    data_value = 44 * i
    url = 'https://s.taobao.com/search?data-key=s&data-value={}&ajax=true&_ksTS={}&callback={}&q={}&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s=44'.format(data_value, _ksTS, callback, key_word)
    get_html_data_from_jsonp(url, G_COOKIE)



# 持久化

f = xlwt.Workbook(encoding='utf-8')
sheet01 = f.add_sheet(u'sheet',cell_overwrite_ok=True)
# 写标题
sheet01.write(0, 0, '标题')
sheet01.write(0, 1, '标价')
sheet01.write(0, 2, '购买人数')
sheet01.write(0, 3, '是否包邮')
sheet01.write(0, 4, '是否天猫')
sheet01.write(0, 5, '地区')
sheet01.write(0, 6, '店名')
sheet01.write(0, 7, 'url')

print(len(DATA))
# 写内容
for i in range(len(DATA)):
    sheet01.write(i+1, 0, DATA[i]['title'])
    sheet01.write(i+1, 1, DATA[i]['view_price'])
    sheet01.write(i+1, 2, DATA[i]['view_sales'])
    sheet01.write(i+1, 3, DATA[i]['view_fee'])
    sheet01.write(i+1, 4, DATA[i]['isTmall'])
    sheet01.write(i+1, 5, DATA[i]['area'])
    sheet01.write(i+1, 6, DATA[i]['name'])
    sheet01.write(i+1, 7, DATA[i]['detail_url'])

f.save(u'search_result.xls')

# 画图
# 1 包邮和不包邮的比例
data1 = {'包邮': 0, '不包邮': 0}
# 2 天猫和淘宝的比例
data2 = {'天猫': 0, '淘宝': 0}
# 3 地区分布
data3 = {}

for item in DATA:
    if item['view_fee'] == '否':
        data1['不包邮'] += 1
    else:
        data1['包邮'] += 1
    if item['isTmall'] == '是':
        data2['天猫'] += 1
    else:
        data2['淘宝'] += 1
    data3[item['area'].split(' ')[0]] = data3.get(item['area'].split(' ')[0], 0) + 1

print(data1)
print(data2)
print(data3)
draw.pie(data1, '是否包邮')
draw.pie(data2, '是否天猫')
draw.bar(data3, '地区分布')
