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
import datetime
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
from tools.tools1 import *


logger = logging.getLogger("oilchemPrice")

# LOGGER.setLevel(logging.CRITICAL)
# 关闭不需要的logger输出
logging.getLogger("easyspider").setLevel("DEBUG")
logging.getLogger("selenium").setLevel("INFO")
logging.getLogger("urllib3").setLevel("INFO")
# logging.getLogger("easyspider").setLevel("INFO")
logging.getLogger("root").setLevel("DEBUG")

logger.info("---code start---")

counter_ = create_counter()

# 用于 schedule.every(10).seconds.do(job1)  # 每隔10s执行下一次任务，函数内部每隔60s执行一次
def weihuabiaoju():
    browser = get_browser()
    print_str("<危化镖局爬取开始！>")
    c = 30
    # _counter = create_counter()  # 重置
    while True:
        durn = weihuabiaoju_one_page(browser)
        if durn <=5:
            #c=counter_() # 每调用一次counter_()，递增一次
            print_str("没获取到数据？ 等待"+str(c)+"分钟再请求！")
            break;
        else:
            print_str("<当前页数据爬取结束！>")
            time.sleep(60)
    browser.quit()
    time.sleep(c*60)
    print_str("<危化镖局睡眠结束！>")

# 用于 每一小时 爬取一次
# schedule.every().day.at('9:30').do(job)
def weihuabiaoju2():
    browser = get_browser()
    print_str("<危化镖局爬取开始！>")

    while True:
        durn = weihuabiaoju_one_page(browser)
        if durn <=5:
            print_str("没获取到数据？等待下一次任务！")
            break;
        else:
            print_str("<当前页数据爬取结束！>")
            time.sleep(60)
    browser.quit()
    print_str("<危化镖局爬取结束！>")

def weihuabiaoju_one_page(browser):
    # 反爬很严重，每次首页只能访问5次左右，然后要间隔半小时后才可以继续访问
    link="https://www.weihuabiaoju.com/ptnpc/index.html#/goods"
    desc="危化镖局"
    starttime = datetime.datetime.now()  # 获得当前时间
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
                code = post('http://beta.napi.huayunquan.com/basic/whbj/simplePublishForPython',param)
                if code != 0:
                    print_str("保存失败：" +goodsId)
                else:
                    print_str("保存成功：" +goodsId)
                print(name + " " + weight + " " + start + " " + end + "\n" + "======================================")
                with open(today_date()+".txt", 'a+') as f:
                    check = hashlib.md5(str(name + weight + start + end).encode("utf-8")).hexdigest()
                    f.write(log_time() + str(code) + " " + check + " " + next_link.text.replace("\n", " ") + "\n")

            except NoSuchElementException as err:
                print(err)

    except Exception as err:
        print(err)
        print_str("抓取异常了，本次终止, 等待1s")
        time.sleep(1)

    endtime = datetime.datetime.now()  # 获得当前时间
    durn = (endtime - starttime).seconds  # 两个时间差，并以秒显示出来
    return durn


def job1():
    # starttime = "09:30:00"
    # endtime = "17:30:00"
    # time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
    # if time_now < starttime:
    #     time_min = time.strftime("%H:%M", time.localtime())
    #     if (time_min == "1:00") or (time_min == "2:00") or (time_min == "3:00") or (time_min == "4:00") or (time_min == "5:00") or (time_min == "6:00") or (time_min == "7:00") or (time_min == "8:00") or (time_min == "9:00") or (time_min == "9:29"):
    #         print("化运圈定时任务睡眠:" + time_min)
    # elif time_now > endtime:
    #     time_min = time.strftime("%H:%M", time.localtime())
    #     if (time_min == "18:00") or (time_min == "19:00") or (time_min == "20:00") or (time_min == "21:00") or (time_min == "22:00") or (time_min == "23:00") or (time_min == "23:59") or (time_min == "17:29"):
    #         print("化运圈定时任务睡眠:"+ time_min)
    # else:
    #     weihuabiaoju()
    print_str("test.....")


import schedule
def main():
    global browser
    print(os.name)
    schedule.every(60).seconds.do(job1)  # 每隔60s执行一次任务

    while True:
        schedule.run_pending()
        time.sleep(1)

    logger.info("end")


if __name__ == '__main__':
    main()






