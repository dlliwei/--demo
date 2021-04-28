import datetime
import time
import requests
import json

def get_time_interval():
    a = datetime.now()  # 获得当前时间
    time.sleep(22)  # 睡眠两秒
    b = datetime.now()  # 获取当前时间
    durn = (b - a).seconds  # 两个时间差，并以秒显示出来
    print(durn)

def today_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
def today_date():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))
def log_time():
    return "[" +today_time()+ "] "
def print_str(str):
    print(log_time() + str)

def create_counter():
    def increase():
        n = 5
        while True:
            n = n + 5
            yield n

    it = increase()
    def counter():
        return next(it)
    return counter

def post(url, param):
    #jsoninfo = json.dumps(dict)  # 输出str类型
    #dictinfo = json.loads(json_str)  # 输出dict类型

    #url = 'http://beta.napi.huayunquan.com/basic/whbj/simplePublishForPython'
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


if __name__ == '__main__':
    _counter = create_counter()
    print_str(str(_counter()))
    print_str(str(_counter()))
    print_str(str(_counter()))
