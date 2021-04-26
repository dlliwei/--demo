from bs4 import BeautifulSoup as bs
import urllib.request


url = "http://www.hellobi.com/"
data = urllib.request.urlopen(url).read().decode("utf-8","ignore")
bs1=bs(data)

#格式化输出
#print(bs1.prettify())

#获取标签
bs1.title
bs1.title.string
bs1.title.name
bs1.a.attrs
bs1.a["class"]
bs1.a.get("class")
bs1.find_all('a')
bs1.find_all(['a','ul'])
k1 = bs1.ul.contents
k2 = bs1.ul.children
allulc=[i for i in k2]

