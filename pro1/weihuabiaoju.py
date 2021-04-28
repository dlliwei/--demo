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
total = 0


# min_time = 1
# max_time = 3

Account = "13918156153"
Password = "molbase2021"

def connect_mysql():
    global server
    server = MysqlService(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT)
    server.select_db(MYSQL_DB)


def today_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
def today_date():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))
def log_time():
    return "[" +today_time()+ "] "
def print_str(str):
    print(log_time() + str)

def j(extract_list):
    return "".join(extract_list.extract()).replace(":", "").strip()

def create_counter():
	def increase():
		n = 5
		while True:
			n = n+5
			yield n
	it = increase()
	def counter():
		return next(it)
	return counter
counter_ = create_counter()

def weihuabiaoju():
    link="https://www.weihuabiaoju.com/ptnpc/index.html#/goods"
    desc="危化镖局"
    starttime = datetime.now()  # 获得当前时间
    print_str("<当前页数据爬取开始！>")
    try:
        browser.get(link)
        for next_link in browser.find_elements_by_xpath('//div[@class="list-container"]/div[@class="list"]/ul'):
            #print(next_link.text.replace("\n", " "))
            try:
                # 发货地
                start_province= next_link.find_element_by_xpath('.//li[@class="start"]/div[@class="province"]').text
                start_city = next_link.find_element_by_xpath('.//li[@class="start"]/div[@class="city"]').text
                start = start_province.replace("-",",")+","+start_city.replace("-",",")
                # 目的地
                end_province = next_link.find_element_by_xpath('.//li[@class="end"]/div[@class="province"]').text
                end_city = next_link.find_element_by_xpath('.//li[@class="end"]/div[@class="city"]').text
                end = end_province.replace("-",",")+","+end_city.replace("-",",")

                # 名称，类别，重量
                name = ""
                weight = ""
                info = next_link.find_element_by_xpath('.//li[@class="goods-info"]').text
                info1 = info.split('-')
                count = len(info1)
                if count == 3:
                    name = info1[0] + "-" + info1[1]
                    weight = info1[2] # 需要是数字
                else:
                    name = info
                    weight = "30"

                # 备注
                price = next_link.find_element_by_xpath('.//li[@class="price"]').text
                pubtime = next_link.find_element_by_xpath('.//li[@class="pub-time"]').text
                remarks = "参考价格:" + str(price) + ",发布时间:"+ str(pubtime)

                # url
                goodsId = next_link.find_element_by_xpath('.//li[@class="pub-time detail-btn"]/div/div').get_attribute("id")
                reptileUrl = "https://www.weihuabiaoju.com/ptnpc/index.html#/goodsdetail?gsid=" + goodsId

                weight_reg = "\d+(\.\d+)?"
                try:
                    weight = re.search(weight_reg, weight).group()
                except Exception as err:
                    weight = "30"

                param = {
                 'goodsName': name,
                 'goodsWight': weight,
                 'deliCity': start,
                 'arriCity': end,
                 'remark': remarks,
                 'reptileUrl': reptileUrl,
                 'reptileSource': desc
                }
                code = post(param)
                if code != 0:
                    print_str("保存失败：" +goodsId)
                else:
                    print_str("保存成功：" +goodsId)
                print(name + " " + weight + " " + start + " " + end + "\n" + "======================================")
                with open(today_date()+".txt", 'a+') as f:
                    f.write(log_time() + str(code) + " " + next_link.text.replace("\n", " ") + "\n")

            except NoSuchElementException as err:
                print(err)

    except Exception as err:
        #msg = traceback.print_exc()
        print(err)
        print_str("抓取异常了，本次终止, 等待1s")
        time.sleep(1)

    endtime = datetime.now()  # 获得当前时间
    durn = (endtime - starttime).seconds  # 两个时间差，并以秒显示出来
    if durn <=5:
        c=counter_()
        print_str("没获取到数据？ 等待"+str(c)+"分钟！")
        browser.quit()
        time.sleep(c*60)
    else:
        print_str("<当前页数据爬取结束！>")

def job1():
    starttime = "09:30:00"
    endtime = "17:30:00"
    time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
    if time_now < starttime:
        time_min = time.strftime("%H:%M", time.localtime())
        if (time_min == "1:00") or (time_min == "2:00") or (time_min == "3:00") or (time_min == "4:00") or (time_min == "5:00") or (time_min == "6:00") or (time_min == "7:00") or (time_min == "8:00") or (time_min == "9:00") or (time_min == "9:29"):
            print("化运圈定时任务睡眠:" + time_min)
    elif time_now > endtime:
        time_min = time.strftime("%H:%M", time.localtime())
        if (time_min == "18:00") or (time_min == "19:00") or (time_min == "20:00") or (time_min == "21:00") or (time_min == "22:00") or (time_min == "23:00") or (time_min == "23:59") or (time_min == "17:29"):
            print("化运圈定时任务睡眠:"+ time_min)
    else:
        weihuabiaoju()





import schedule

def main():
    global browser
    option = webdriver.ChromeOptions()
    print(os.name)
    schedule.every(1).seconds.do(job1)  # 每隔10s执行一次任务

    # 设置IP代理
    # thisapi = 'http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=1&fa=0&groupid=0&fetch_key=&time=1&qty=19&port=1&format=txt&ss=1&css=&dt=&pro=&city=&usertype=4'
    # ippools = urllib.request.urlopen(thisapi).read().decode("utf-8", "ignore")
    # ipchoose = random.choice(ippools.split("\r\n"))
    # print("======== IP代理：" + ipchoose)
    # option.add_argument("--proxy-server="+ipchoose)

    # 设置用户代理
    uapools = [
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 QIHU 360EE",
    ]
    thisua = random.choice(uapools)
    option.add_argument("User-Agent="+thisua)

    path = r"huayunquanx"
    option.add_argument('user-data-dir=%s' % path)
    option.add_argument('log-level=3')
    option.add_argument('disable-gpu')
    browser = webdriver.Chrome("../chromedriver.exe", options=option)


    while True:
        schedule.run_pending()
        time.sleep(1)

    logger.info("end")
    browser.quit()

def post(param):
    #jsoninfo = json.dumps(dict)  # 输出str类型
    #dictinfo = json.loads(json_str)  # 输出dict类型

    url = 'http://beta.napi.huayunquan.com/basic/whbj/simplePublishForPython'
    # paramTest = {"goodsName": "测试1",
    #              "goodsWight": "31",
    #              "deliCity": "辽宁省,抚顺市",
    #              "arriCity": "黑龙江省,大庆市",
    #              "remark": "参考价格:160元,发布时间:1分钟前",
    #              "reptileUrl": "https://www.weihuabiaoju.com/ptnpc/index.html#/goodsdetail?gsid=5402533403",
    #              "reptileSource": "危化镖局"}
    res = requests.post(url, json=param)  # 接口调用
    resTest = json.loads(res.text)  # 将返回结果str转成dict
    # {'code': 0, 'message': 'Success', 'data': None}
    #print(resTest)
    return resTest['code']


def demo():
    global browser
    option = webdriver.ChromeOptions()
    browser = webdriver.Chrome("../chromedriver.exe")
    browser.get("E:/projPy/molbase/huayunquan/demo.html")
    for next_link2 in browser.find_elements_by_xpath('//div[@class="list-container"]/div[@class="list"]/ul'):
        #print(next_link2.text.replace("\n", " "))
        try:
            # 发货地
            #bannner = next_link2.find_element_by_xpath('.//li[@class="banner"]').text

            start_province = next_link2.find_element_by_xpath(
                './/li[@class="start"]/div[@class="province"]').text
            start_city = next_link2.find_element_by_xpath('.//li[@class="start"]/div[@class="city"]').text
            start = start_province + "," + start_city
            # 目的地
            end_province = next_link2.find_element_by_xpath('.//li[@class="end"]/div[@class="province"]').text
            end_city = next_link2.find_element_by_xpath('.//li[@class="end"]/div[@class="city"]').text
            end = end_province + "," + end_city

            print(start + " " + end )
            print("=========")
        except NoSuchElementException as err:
            print(err)

    browser.quit()

def get_time_interval():
    a = datetime.now()  # 获得当前时间
    time.sleep(22)  # 睡眠两秒
    b = datetime.now()  # 获取当前时间
    durn = (b - a).seconds  # 两个时间差，并以秒显示出来
    print(durn)

if __name__ == '__main__':
    #main()
    demo()





