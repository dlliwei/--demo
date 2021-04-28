import urllib.request
import http.cookiejar


def main():
    # cookie 读取
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    urllib.request.install_opener(opener)
    print(str(cjar)) #cookie读取

    # header设置
    # 有些网站需要伪装成网页，才允许爬虫，例如：
    # urllib.request.urlopen("http://www.qiushibaike.com")
    # 返回 “Remote end closed connection without response”
    # 是怎么判断 请求是不是网页的呢？ 通过参数 "User-Agent"
    # 所以爬虫时 要设置User-Agent

    # 方式一
    url = "http://www.qiushibaike.com"
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders=[headers]
    data = opener.open(url).read()
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read()

    # 多个header
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Content-Type": "application/javascript",
    }
    opener = urllib.request.build_opener()
    headall = []
    for key, value in headers.items():
        item = (key,value)
        headall.append(item)
    opener.addheaders = headall
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read()


    # 方式三
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
    reqdata = urllib.request.urlopen(req).read().decode("utf-8","ignore")






if __name__ == '__main__':
    main()