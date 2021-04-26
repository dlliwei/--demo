import urllib.request
import http.cookiejar
import pymysql
import re
import traceback
import random

# 获取淘宝图片  失败


keyname="维维豆奶"
key = urllib.request.quote(keyname)
def main():

    for i in range(1,10):
        '''
        搜索结果页： https://s.taobao.com/search?q=维维豆奶&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306
        选择第二页： https://s.taobao.com/search?q=维维豆奶&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s=44
        选择第三页： https://s.taobao.com/search?q=维维豆奶&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s=88
        那么第N页简化：https://s.taobao.com/search?q=维维豆奶&s=44(N-1)
        '''
        try:
            print("========== page "+str(i) + "=========")
            url = "https://s.taobao.com/search?q="+ key +"&s=" + str(44*(i-1))
            data = urllib.request.urlopen(url).read().decode("utf-8","ignore")
            pat = '"pic_url":"//(.*?)"'
            imglist = re.compile(pat).findall(data)
            for j in range(0, len(imglist)):
                try:
                    thisimg = imglist[j]
                    thisimgurl = "http://" +thisimg
                    localfile = "E:/data/taobao/" + str(i) + "_" + str(j) + "jpg"
                    urllib.request.urlretrieve(thisimgurl, filename=localfile)
                except Exception as err:
                    pass
        except Exception as err:
            pass
    print("========== end all =========")

if __name__ == '__main__':
    main()