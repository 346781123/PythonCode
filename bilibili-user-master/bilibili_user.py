# -*-coding:utf8-*-

import requests
import json
import random
import pymysql
import sys
import datetime
import time
from imp import reload
from multiprocessing.dummy import Pool as ThreadPool

def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()


reload(sys)


def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas


uas = LoadUserAgents("user_agents.txt")
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

# Please replace your own proxies.
proxies = {
    'http': 'http://117.141.155.242:53281',
    'http': 'http://1.192.243.35:9999',
    'http': 'http://124.207.82.166:8008',
}
time1 = time.time()

urls = []

# Please change the range data by yourself.
start = int(sys.argv[1])
end = int(sys.argv[2])
for m in range(start, end):

    for i in range(m * 100, (m + 1) * 100):
        url = 'https://space.bilibili.com/' + str(i)
        urls.append(url)


    def getsource(url):
        mid = url.replace('https://space.bilibili.com/', '')
        payload = {
            '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
            'mid': mid
        }
        ua = random.choice(uas)
        head = {
            'User-Agent': ua,
            'Referer': 'https://space.bilibili.com/' + str(mid) + '?from=search&seid=' + str(random.randint(10000, 50000))
        }
        jscontent = requests\
            .get('https://api.bilibili.com/x/space/acc/info?mid='+str(mid),headers=head,params=payload,proxies=proxies) \
            .text
        time2 = time.time()
        try:
            jsDict = json.loads(jscontent)
            statusJson = True if 'code' in jsDict.keys() else False
            if statusJson == True:
                if 'data' in jsDict.keys():
                    jsData = jsDict['data']
                    mid = jsData['mid']
                    name = jsData['name']
                    sex = jsData['sex']
                    rank = jsData['rank']
                    face = jsData['face']
                    regtimestamp = jsData['jointime']
                    regtime_local = time.localtime(regtimestamp)
                    regtime = time.strftime("%Y-%m-%d %H:%M:%S",regtime_local)
                    birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                    sign = jsData['sign']
                    level = jsData['level']
                    OfficialVerifyType = jsData['official']['title']
                    OfficialVerifyRole = jsData['official']['role']
                    OfficialVerifyDesc = jsData['official']['desc']
                    vipType = jsData['vip']['type']
                    vipStatus = jsData['vip']['status']
                    vipThemeType = jsData['vip']['theme_type']
                    toutu = jsData['top_photo']
                    spacesta = 0
                    toutuId = 0
                    coins = jsData['coins']
                    print("Succeed get user info: " + str(mid) + "\t" + str(time2 - time1))
                    try:
                        res = requests.get(
                            'https://api.bilibili.com/x/relation/stat?vmid=' + str(mid) + '&jsonp=jsonp').text
                        viewinfo = requests.get(
                            'https://api.bilibili.com/x/space/upstat?jsonp=jsonp&mid=' + str(mid),headers=head,proxies=proxies).text
                        js_fans_data = json.loads(res)
                        js_viewdata = json.loads(viewinfo)
                        following = js_fans_data['data']['following']
                        fans = js_fans_data['data']['follower']
                        archiveview = js_viewdata['data']['archive']['view']
                        article = js_viewdata['data']['article']['view']
                    except:
                        following = 0
                        fans = 0
                        archiveview = 0
                        article = 0
                else:
                    print('no data now')
                try:
                    # Please write your MySQL's information.
                    conn = pymysql.connect(
                        host='localhost', user='root', passwd='root', db='bilibili', charset='utf8')
                    cur = conn.cursor()
                    cur.execute('INSERT INTO bilibili_user_info(mid, name, sex, rank, face, regtime, spacesta, \
                                birthday, sign, level,OfficialVerifyRole, OfficialVerifyType, OfficialVerifyDesc, vipType, vipStatus, \
                                toutu, toutuId, coins, following, fans ,archiveview, article) \
                    VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",\
                            "%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s")'
                                %
                                (mid, name, sex, rank, face, regtime, spacesta, \
                                birthday, sign, level, OfficialVerifyRole,OfficialVerifyType, OfficialVerifyDesc, vipType, vipStatus, \
                                toutu, toutuId, coins, following, fans ,archiveview, article))
                    conn.commit()
                except Exception as e:
                    print(e)
            else:
                print("Error: " + url)
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":

    pool = ThreadPool(4)
    try:
        results = pool.map(getsource, urls)
    except Exception as e:
        print(e)

    pool.close()
    pool.join()

