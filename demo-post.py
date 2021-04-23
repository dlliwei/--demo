import urllib.request
import urllib.parse
import re


def main():

    url = "http://www.iqianyue.com/mypost"
    postdata = urllib.parse.urlencode({
        "name":"ceo@iqianyue.com",
        "pass":"aA123456"
    }).encode('urf-8')

    req = urllib.request.Request(url, postdata)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36')
    data = urllib.request.urlopen(req).read()
    fhandle = open("E:/desktop/temp/posttest.html", "wb")
    fhandle.write(data)
    fhandle.close()






if __name__ == '__main__':
    main()