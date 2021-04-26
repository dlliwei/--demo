# -*- coding: utf-8 -*-
# @Author: liwei
# 13918156153 molbase2021
# @Date:   2019-12-27 10:03:47
# @Last Modified by:   liwei
# @Last Modified time: 2021-04-22 14:47:18
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import urllib
from datetime import datetime
import re
from scrapy import Selector
import random
#import easylogger
import logging
import pdb
import traceback
import hashlib
from easyspider.pipelines.commonMysqlpipeline import process_item
from DBService import MysqlService
import json
from selenium import webdriver
import time
import os
import sys
import requests

# reload(sys)
# sys.setdefaultencoding("utf-8")
"""
mac 上启动测试

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --flag-switches-begin --flag-switches-end --enable-audio-service-sandbox --user-data-dir=/Users/zhanghang/Downloads/chrome https://www.baidu.com/

如果百度没有桌面的话，就是错的，就要重新来一次了

sudo cp -R /Users/zhanghang/Library/Application\ Support/Google/Chrome/Default /Users/zhanghang/Downloads/chrome



https://dc.oilchem.net/price_search/list.htm?businessType=2&varietiesName=%E6%BA%B4%E7%B4%A0&varietiesId=3711&templateType=1&flagAndTemplate=1-1&channelId=2685&isShow=0&oneName=%E5%8C%96%E8%82%A5&twoName=%E6%BA%B4%E7%B4%A0

"""


# $x('//*[@id="navfist_3"]//*[@class="nav_class_third"]//a').map((x)=>{return x.href}).join("\n")

#easylogger.init(None)
logger = logging.getLogger("oilchemPrice")

# LOGGER.setLevel(logging.CRITICAL)
# 关闭不需要的logger输出
logging.getLogger("easyspider").setLevel("DEBUG")
logging.getLogger("selenium").setLevel("INFO")
logging.getLogger("urllib3").setLevel("INFO")
# logging.getLogger("easyspider").setLevel("INFO")
logging.getLogger("root").setLevel("DEBUG")

logger.info("---code start---")
MYSQL_HOST = "122.226.111.10"
MYSQL_USER = "db_rw"
MYSQL_PASSWORD = "molbase1010"
MYSQL_PORT = 3306
MYSQL_DB = "baike_bak"

server = None
browser = None

min_time = 6
max_time = 9


# min_time = 1
# max_time = 3

Account = "13918156153"
Password = "molbase2021"

def connect_mysql():
    global server
    server = MysqlService(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT)
    server.select_db(MYSQL_DB)


def _today_date():
    # return "2019-11-01"
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))

#x.xpath("./ul[@class='list']/li").extract()
#extract使提取内容转换为Unicode字符串，返回数据类型为list
def j(extract_list):
    return "".join(extract_list.extract()).replace(":", "").strip()



# def login(wd):
#     #login_url = 'http://passport.lianjia.com/cas/login?service=http%3A%2F%2Fuser.sh.lianjia.com%2Findex'
#     #wd.get(login_url)
#
#     wd.find_element_by_xpath('*//div[@id="tab-second"]').click()
#     wd.find_element_by_xpath('//*[@type="phone"]').send_keys(Account)
#     wd.find_element_by_xpath('//*[@type="password"]').send_keys(Password)
#     wd.find_element_by_xpath('//*[@class="el-form-item__content"/button').click()
#
#     req = requests.Session() #构建Session
#     global Cookies
#     Cookies = wd.get_cookies() #导出cookie

def run_in_one_page(link):
    try:

        browser.get(link)
        time.sleep(random.randint(min_time, max_time))

        # return
        # 然后点击本页的其他价格分类
        # pdb.set_trace()
        for next_link in browser.find_elements_by_xpath('//div[@class="list-container"]/div[@class="list"]/ul'):
            #print(next_link.text)
            # 发货地
            start_province= browser.find_element_by_xpath('//li[@class="start"]/div[@class="province"]').text
            start_city = browser.find_element_by_xpath('//li[@class="start"]/div[@class="city"]').text
            start = start_province+","+start_city
            #目的地
            end_province = browser.find_element_by_xpath('//li[@class="end"]/div[@class="province"]').text
            end_city = browser.find_element_by_xpath('//li[@class="end"]/div[@class="city"]').text
            end = end_province+","+end_city

            # 名称，类别，重量
            name = info
            weight = "30"
            info = browser.find_element_by_xpath('//li[@class="goods-info"]').text
            info1 = info.split('-')
            count = len(info1)
            if count == 3:
                name = info1[0] + "-" + info1[1]
                weight = info1[2] # 需要是数字

            # 备注
            price = browser.find_element_by_xpath('//li[@class="price"]').text
            pubtime = browser.find_element_by_xpath('//li[@class="pub-time"]').text
            remarks = "参考价格:" + str(price) + ",发布时间:"+ str(pubtime)

            print("发货地：" + start)
            print("目的地：" + end)
            print("货物名称：" + name)
            print("重量：" + weight )
            print("备注：" + remarks)
            weight_reg = "\d+(\.\d+)?"
            try:
                weight = re.search(reg, weight).group()
            except Exception as err:
                weight = "30"


            headers = {'Content-Type': 'application/json'}  # 消息头，根据实际需要添加
            url = 'http://beta.napi.huayunquan.com/basic/whbj/simplePublishForPython'  # 地址
            param = {
             'goodsName': info,
             'goodsWight': weight,
             'deliCity': start,
             'arriCity': end,
             'remark': remarks,
             'reptileUrl': link,
             'reptileSource': "危化镖局"
            }
            paramTest = {
                'goodsName': '燃料油-三类',
                'goodsWight': '',
                'deliCity': '抚顺市,辽宁省',
                'arriCity': '大庆市,黑龙江省',
                'remark': '参考价格:160元,发布时间:1分钟前',
                'reptileUrl': 'https://www.weihuabiaoju.com/ptnpc/index.html#/goods',
                'reptileSource': "危化镖局"
            }
            dataJson = json.dumps(param)  # 将 dict转成str
            res = requests.post(url, data=paramTest, headers=headers)  # 接口调用

            resTest = json.loads(res.text)  # 将返回结果str转成dict
            print(resTest)
            time.sleep(5) #每5秒插入一次



    except Exception:
        msg = traceback.print_exc()
        print(msg)
        # pdb.set_trace()

def get_req():
    global Req
    global Cookies
    if Req:
        return Req
    Req = requests.Session()  # 构建Session
    for cookie in Cookies:
        Req.cookies.set(cookie['name'], cookie['value'])  # 转换cookies
    return Req

def do_request(url):
    req = get_req()
    for i in range(5):
        try:
            res = req.get(url)
        except (ConnectionResetError, requests.exceptions.ConnectionError):
            print('open %s failed and try %sth in 5s' % (url, i+2))
            time.sleep(5)
        else:
            break
    return res

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
            data = urllib.request.urlopen("http://baidu.com")
            data1 = data.read().decode("utf-8","ignore")
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


def main():
    # with open("all_link.txt") as f:
    #     content = list(map(lambda x: x.strip(), f.readlines()))



    global browser
    connect_mysql()
    option = webdriver.ChromeOptions()
    print(os.name)

    # 设置代理
    thisapi = 'http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=7&fa=1&groupid=0&fetch_key=&time=1&qty=200&port=1&format=txt&ss=1&css=&dt=&pro=&city=&usertype=4'
    ippools = urllib.request.urlopen(thisapi).read().decode("utf-8", "ignore")
    ipchoose = random.choice(ippools.split("\r\n"))
    print("======== IP代理：" + ipchoose)
    option.add_argument("--proxy-server="+ipchoose)


    if os.name == "nt":
        path = r"huayunquanx"
        option.add_argument('user-data-dir=%s' % path)
        option.add_argument('log-level=3')
        option.add_argument('disable-gpu')
        # --disable-gpu
        browser = webdriver.Chrome("chromedriver.exe", options=option)
    elif os.name == "posix":
        path = "/Users/zhanghang/Downloads/chrome"
        option.add_argument('user-data-dir=%s' % path)
        option.add_argument('log-level=3')
        browser = webdriver.Chrome(
            "/Users/zhanghang/Downloads/chromedriver", options=option)
    logger.info("wait for login")
    browser.implicitly_wait(60)

    url="https://www.weihuabiaoju.com/ptnpc/index.html#/goods"
    run_in_one_page(url)

   # rate, all_count = 1, len(content)


    # for line in content:
    #     try:
    #         run_in_one_page(line)
    #         logger.info("[%d / %d]" % (rate, all_count))
    #     except ElementNotInteractableException:
    #         logger.info("error ElementNotInteractableException [%d / %d]" % (rate, all_count))
    #         msg = traceback.format_exc()
    #         print(msg)
    #         # pdb.set_trace()
    #     except NoSuchElementException:
    #         logger.info("error NoSuchElementException [%d / %d]" % (rate, all_count))
    #     rate += 1
    logger.info("end")
    browser.quit()

def post(start,end,info,remarks,link):
    headers = {'Content-Type': 'application/json'}  # 消息头，根据实际需要添加
    url = 'http://beta.napi.huayunquan.com/basic/whbj/simplePublishForPython'  # 地址
    param = {
        'goodsName': info,
        'goodsWight': '',
        'deliCity': start,
        'arriCity': end,
        'remark': remarks,
        'reptileUrl': link,
        'reptileSource': "危化镖局"
    }
    paramTest = {
        'goodsName': '燃料油-三类',
        'goodsWight': '',
        'deliCity': '抚顺市,辽宁省',
        'arriCity': '大庆市,黑龙江省',
        'remark': '参考价格:160元,发布时间:1分钟前',
        'reptileUrl': 'https://www.weihuabiaoju.com/ptnpc/index.html#/goods',
        'reptileSource': "危化镖局"
    }
    dataJson = json.dumps(paramTest)  # 将 dict转成str
    res = requests.post(url, paramTest, headers)  # 接口调用
    print(res.status_code)
    resTest = json.loads(res.text)  # 将返回结果str转成dict
    print(resTest)

if __name__ == '__main__':
    #main()
    # post(1,1,1,1,1)
    info0 = ""

    reg = "\d+(\.\d+)?"
    price = re.search(reg, info0).group()
    print(price)

    print("")
