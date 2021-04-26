import urllib.request
import http.cookiejar
import pymysql
import re
import traceback
import random
from bs4 import BeautifulSoup as bs
import time

# -*- coding: UTF-8 -*-

'''
IP代理方案一:
IP代理方案二：见视频，需要花钱购买IP代理
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
]

# IP代理方案一
def ip(ippools):
    thisip = random.choice(ippools)
    print(thisip)
    proxy = urllib.request.ProxyHandler({"http":thisip})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    #安装为全局
    urllib.request.install_opener(opener)

# IP代理方案二：接口调用可用IP
# thisapi 即 花钱购买的IP的接口地址
def use_ip(iptools, myurl, thisapi):
    def api(thisapi):
        import urllib.request
        print("这一次调用了接口")
        import urllib.request
        urllib.request.urlcleanup()
        thisapi=urllib.request.urlopen(thisapi).read().decode("utf-8","ignore")
        print("接口调用完成")
    def ip(iptools):
        thisapi=iptools
        print("当前调用的IP是：" + iptools)
        proxy=urllib.request.ProxyHandler({"http": thisapi})
        opener=urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
    if(iptools==0):
        ippools=api(thisapi)
        print("提取IP完成")
    ip(iptools)
    url=myurl
    data=urllib.request.urlopen(url).read().decode("gbk","ignore")
    return iptools,data


# use_ip 升级版本，增加：判断ip是否有效判断
def use_ip_upgrade(ippools, myurl, thisapi):
    def api(thisapi):
        import urllib.request
        print("这一次调用了接口")
        import urllib.request
        urllib.request.urlcleanup()
        thisall=urllib.request.urlopen(thisapi).read().decode("utf-8","ignore")
        print("接口调用完成")
        return thisall
    def ip(ippools):
        thisapi=ippools
        print("当前调用的IP是：" + ippools)
        proxy=urllib.request.ProxyHandler({"http": thisapi})
        opener=urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
    if(ippools==0):
        while True:
            ippools=api(thisapi)
            print("提取IP完成")
            ip(ippools)
            print("正在验证IP有效性")
            data = urllib.request.urlopen("htpp://www.baidu.com").read().decode("utf-8","ignore")
            if(len(data) > 5000):
                print("------- 当前IP有效 ------")
                break
            else:
                print("------- 当前IP无效，正在延时60秒重新切换 ------")
                time.sleep(15)
    else:
        ip(ippools)
    url=myurl
    data=urllib.request.urlopen(url).read().decode("gbk","ignore")
    return ippools,data


# IP代理方案三：自建服务器+自动切换IP技术





thisapi='http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=1&fa=0&groupid=0&fetch_key=&time=1&qty=200&port=1&format=txt&ss=1&css=&dt=&pro=&city=&usertype=4'
def main():
    for i in range(1, 10):
        try:
            url = "http://www.baidu.com"
            if(i%7==0 and i==0):
               iptools,thispagedata=use_ip_upgrade(0, url, thisapi)
            elif (i%7 == 0):
                print("正在延时中...")
                time.sleep(15)
                print("延时完成，正在调取IP")
                iptools, thispagedata = use_ip_upgrade(0, url, thisapi)
                print("IP调取完成")
            else:
               iptools, thispagedata = use_ip_upgrade(iptools, url, thisapi)
            print(len(thispagedata))
        except Exception as err:
            print(err)


    print("========== end all =========")







if __name__ == '__main__':
    main()