
import urllib.request
import re


def main():
    # 爬到内存中，方法一
    data =  urllib.request.urlopen("https://edu.hellobi.com/course/211").read().decode("utf-8", "ignore")
    # 拿到状态码
    print(data.getcode())


    # 爬到内存中，方法二
    url = "http://www.baidu.com"
    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req).read().decode("utf-8", "ignore")

    pat = "<title>(.*?)</title>"
    title = re.compile(pat, re.S).findall(data)

    # 爬到硬盘中
    urllib.request.urlretrieve(url,filename="E:/desktop/temp/1.txt")

    # url请求中如果有中文
    key_code = urllib.request.quote("马蹄糕")




if __name__ == '__main__':
    main()