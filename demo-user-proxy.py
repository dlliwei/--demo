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
用户代理： 同一个IP，但是是不同的浏览器
'''


keyname="维维豆奶"
key = urllib.request.quote(keyname)
uapools = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 QIHU 360EE",
]

# 用户代理
def ua(uapools):
    thisua = random.choice(uapools)
    print(thisua)
    headers = ("User-Agent", thisua)
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    #安装为全局
    urllib.request.install_opener(opener)

def main():
    fh = open("E:/data/baidu/list.txt", "w")
    for i in range(1, 10):
        '''
        使用用户代理：ua(uapools)
        '''
        ua(uapools)

        print("========== page "+str(i) + "=========")
        url = "https://www.baidu.com/s?wd="+key+"&pn=" + str(10*(i-1))
        data = urllib.request.urlopen(url).read().decode("utf-8","ignore")
        pat = 'data-tools=\'{"title":"(.*?)","url":".*?"}\''
        list = re.compile(pat).findall(data)

        for j in range(0, len(list)):
            fh.write("[page "+str(i)+"]\n" + str(list[j]))
            print(str(list[j]))

    fh.close()
    print("========== end all =========")







    localfile = "E:/data/demo-cookie-header.xml"
    urllib.request.urlretrieve(url, filename=localfile)



if __name__ == '__main__':
    main()