import urllib.request
import http.cookiejar
import pymysql
import re
import traceback
import random
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
import requests

# -*- coding: UTF-8 -*-

'''
用户代理 + IP代理
'''

keyname="维维豆奶"
key = urllib.request.quote(keyname)
ippools = [
    "49.88.210.22:45102",
    "180.126.190.133:45105",
    "222.37.107.38:46603",
    "175.167.21.123:45120",
    "114.220.38.67:45118",
    "119.36.157.230:24093",
    "222.37.130.192:46603",
    "182.34.206.154:18950",
    "58.213.26.149:45117",
    "123.73.81.113:46603",
    "127.0.0.1:8888",
]

# IP代理方案一
def ip(ippools):
    thisip = random.choice(ippools)
    print(thisip)
    proxy = urllib.request.ProxyHandler({"http":thisip})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    #安装为全局
    urllib.request.install_opener(opener)


def use_ip_upgrade(ippools, myurl, thisapi):
    uapools = [
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 QIHU 360EE",
    ]
    def api(thisapi):
        import urllib.request
        print("这一次调用了接口")
        import urllib.request
        urllib.request.urlcleanup()
        thisall=urllib.request.urlopen(thisapi).read().decode("utf-8","ignore")
        print("接口调用完成")
        return thisall
    def ip(ippools,uapools):
        thisua = random.choice(uapools)
        print("当前调用的ua是：" + thisua)
        headers = ("User-Agent", thisua)

        thisip = ippools
        # thisapi= "127.0.0.1:8888"
        print("当前调用的IP是：" + thisip)
        proxy = urllib.request.ProxyHandler({"http": thisip})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        opener.addheaders = [headers]
        urllib.request.install_opener(opener)
    if(ippools==0):
        while True:
            ippools=api(thisapi)
            print("提取IP完成")
            ip(ippools,uapools)
            print("正在验证IP有效性")
            data = urllib.request.urlopen("http://baidu.com").read().decode("utf-8","ignore")
            if(len(data) > 5000):
                print("------- 当前IP有效 ------")
                break
            else:
                print("------- 当前IP无效，正在延时60秒重新切换 ------")
                time.sleep(60)
    else:
        ip(ippools)

    url=myurl
    data=urllib.request.urlopen(url).read().decode("gbk","ignore")
    return ippools,data



thisapi='http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=1&fa=0&groupid=0&fetch_key=&time=1&qty=200&port=1&format=txt&ss=1&css=&dt=&pro=&city=&usertype=4'
def main():

    url = "https://www.weihuabiaoju.com/ptnpc/index.html#/goods"

    for i in range(0, 35):
        try:
            if(i%5==0 and i==0):
               iptools,thispagedata=use_ip_upgrade(0, url, thisapi)
            elif (i%5 == 0):
                print("正在延时中...")
                time.sleep(15)
                print("延时完成，正在调取IP")
                iptools, thispagedata = use_ip_upgrade(0, url, thisapi)
                print("IP调取完成")
            else:
               iptools, thispagedata = use_ip_upgrade(ippools, url, thisapi)
            print(len(thispagedata))
        except Exception as err:
            print(err)


    print("========== end all =========")







if __name__ == '__main__':
    main()