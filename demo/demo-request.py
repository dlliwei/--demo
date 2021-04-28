import requests
import re

'''
get, post, put...
参数：params(用于get), headers, proxies, cookies, data(用于post)
'''

def main():
    rsp = requests.get("http://www.baidu.com")
    print(len(rsp.text))
    print(len(rsp.content)) # 二进制数据
    print(rsp.url)
    print(rsp.encoding)
    print(rsp.cookies)
    print(requests.utils.dict_from_cookiejar(rsp.cookies)) # 将cookies转为字典格式
    print(rsp.status_code)

    ck=requests.utils.dict_from_cookiejar(rsp.cookies)
    hd = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    px={"http":"http://127.0.0.1:8888",
        "https": "http://127.0.0.1:8888",
    }
    key={"wd":"喂喂"}
    #rsp = requests.get("http://www.baidu.com", headers=hd, cookies=ck, proxies=px)
    rsp = requests.get("http://www.baidu.com", headers=hd, cookies=ck, params=key)
    title = re.compile("<title>(.*?)</title>", re.S).findall(rsp.text)
    print(title)



    postdata={"name":"", "pass":""}
    requests.post("http://www.baidu.com", data=postdata)




if __name__ == '__main__':
    main()