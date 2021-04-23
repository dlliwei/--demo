import urllib.request
import http.cookiejar
import pymysql
import re
import traceback

# http://www.qiushibaike.com
# 获取热门段子

def main():
    for i in range(1,10):
        try:
            print("--------------page index："+str(i)+"---------------")
            url = "https://www.qiushibaike.com/8hr/page/" + str(i) + "/"
            req = urllib.request.Request(url)
            req.add_header("User-Agent",
                           "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
            data = urllib.request.urlopen(req).read().decode("utf-8", "ignore")

            # 解析 <a class="recmd-content" href="/article/124260744" target="_blank" onclick="_hmt.push(['_trackEvent','web-list-user','chick'])">摄像头拆懂？</a>
            pat = '<a class="recmd-content" .*?>(.*?)</a>'
            rst = re.compile(pat, re.S).findall(data)
            for j in range(0, len(rst)):
                print(">>>>> " + str(j) +": " + rst[j])
        except Exception:
            msg = traceback.print_exc()
            print(msg)




if __name__ == '__main__':
    main()