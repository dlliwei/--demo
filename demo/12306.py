import urllib.request
import http.cookiejar
import ssl
import re
import requests
import gzip

'''
2021.5.8 add for liwei
https://www.12306.cn/
目标任务：自动抢票
先正常订一遍票， 并把各种数据包整理出来，一次摸清请求这些网址并模拟相关数据，并对关键环节进行自动控制。
'''
USERNAME = "15821245821"
PASSWORD = "12306hgbiba984617"
def getxy(pic):
    if(pic==1):
        xy=(35,45)
    if(pic==2):
        xy=(112,45)
    if(pic==3):
        xy=(173,45)
    if(pic==4):
        xy=(253,45)
    if(pic==5):
        xy=(35,114)
    if(pic==6):
        xy=(112,114)
    if(pic==7):
        xy=(173,114)
    if(pic==8):
        xy=(253,114)
    return xy

def main():
    # 为了防止ssl出现问题，你可以加上下面一行代码
    # ssl._create_default_https_context = ssl._create_unverified_context()

    # ---------------------查票----------------------
    # 常用三字码与站点对应关系
    areatocode = {"上海": "SHH", "北京": "BJP", "南京": "NJH", "昆山": "KSH", "杭州": "HZH", "桂林": "GLZ"}
    # start1 = input("请输入起始站:")  # 北京
    # start = areatocode[start1]
    # to1 = input("请输入到站:") # 上海"
    # to = areatocode[to1]
    # isstudent = input("是学生吗？(是：1，不是：0) ")
    # date = input("请输入要查询的乘车开始日期的年月，如2017-03-05：")
    # if (isstudent == "0"):
    #     student = "ADULT"
    # else:
    #     student = "0X00"

    start="SHH"
    to="BJP"
    date="2021-05-09"
    student = "ADULT"

    # https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2021-05-08&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=BJP&purpose_codes=ADULT
    query_url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date="+date+"&leftTicketDTO.from_station="+start+"&leftTicketDTO.to_station="+to+"&purpose_codes="+student
    #context = ssl._create_unverified_context()

    headers = {
        "Host": "kyfw.12306.cn",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "If-Modified-Since": "0",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E4%B8%8A%E6%B5%B7,SHH&date=2021-05-08&flag=N,N,Y",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cookie": "JSESSIONID=E5F5CBC71236A476BFAFF2EF686BEB6F; RAIL_EXPIRATION=1620688040394; RAIL_DEVICEID=cDEcudZLAA4w4ID9X9IGLLszRXNUpbI1ypbXMwSmChKCNVFyLmps-JBdewhJVPkZdjcUd7FJjTNyrqnDkW0amcgp3Gne02n9VpLMvfa9i5D76Sku0PcoHwVdbxX95uXZLz8dSzZVCB5dzZ_wyG0csiSJWvTQHFvL; BIGipServerpool_passport=165937674.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerpassport=937951498.50215.0000; BIGipServerotn=1039139338.64545.0000; BIGipServerpool_statistics=652280330.45094.0000; current_captcha_type=C; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2021-05-08; _jc_save_toDate=2021-05-08; _jc_save_wfdc_flag=dc",
    }
    query_result = urllib.request.urlopen(urllib.request.Request(query_url, headers=headers))
    #query_result2 = query_result.read().decode('utf-8', 'ignore')
    # 处理 gzip 压缩的字符串
    encoding = query_result.info().get('Content-Encoding')
    if encoding == 'gzip':
        content = gzip.decompress(query_result.read())
    else:
        content = query_result.read()
    data_dict = json.loads(content)
    allcheci = ['n%2BdmlrqNoer4uixKCyLVDQwqZHfjYBpcmxc3N501XUu8vsNajA6WsIEYV1giZqzV9qBDyUBI4vlr%0ARoXX3qAS2nMLgtLXBK%2FUHb6okn%2F7UhDho1AKegt%2F9BEo3uu1tnYsnC5L590TsW5cg9XLVnAn7HBw%0AbNLmPcu2yBZDnPK4TkPFRLAHjUkkD8l2%2F6NlbmkEsi1HoxKgCjiDnqK3tRBZ%2BxwHINREF%2BAvdKD9%0ACpBsup%2BtXPSKsbwPzxbEJkJ3wkrYzvrSSB51d%2BhWYTgMWN9hP0SJSSu9GqiB%2BWZ6M43SgYjHbCgp%0A31LXrhR%2FPfk%3D|预订|5l0000G10200|G102|AOH|VNP|AOH|VNP|06:26|12:29|06:03|Y|U517oINxxZi7IIumPHVhWXkRrYKfQcdwKFq886lvm9nijrH%2B|20210509|3|HZ|01|11|1|0|||||||||||有|有|15||O0M090|OM9|1|0||O049800021M0837000219174800015|0|||||1|0#1#0|', '0K%2Byx%2F%2F45M%2BjGoCQigT0GCdWtTwNof4cvFJne7dPdo4tctYKEgdl5K7Gyu13PJ1RrWZfWXguPbWW%0ACf9Mpjc0ziCJjRoXs3yE8PoEHWF37JlokH1V0j0g2wEPXt%2BG%2FbWMLw9QMiq8mF3qNfIQXw0cKbZ0%0ALCsROm%2Fccxd5EteBQA4zGZCtAde8Ynl1eLFIscfqOi7xxLWzkVlPQstk%2FZJCEPhLPJgBr46SorcQ%0AnOxYPwyCYijNrAwRv51cEaBkOsqJbsA6LTeIn%2BC%2FFi%2FCH8l09R0rEk9ux7KHXyflIqxYvgl8eB80%0A4EjQJB1a%2BCs%3D|预订|5l0000G10481|G104|AOH|VNP|AOH|VNP|06:37|12:33|05:56|Y|lnjobNDaIBgE5n2%2FraVotElYus7C2QNBapGNdZG7ixaVnUii|20210509|3|HZ|01|09|1|0|||||||||||有|有|20||O0M090|OM9|1|0||O055300021M0930000219174800020|0|||||1|#0#0|', '1SwSjD39Cv7ZbKTQ4NUE%2B0pWNz9s2ousJv80K21KYVeDL9VOBVqWsDbEk0aRDfEdRBYK8EQW6E%2BW%0AYUPYbXQnUHUdgBPVjl9C%2FIfyKIsaAKkEwpDiRRF%2FmFhLBgsxgM5%2FYeRUPW82C2U2ggkfCfPwp%2FMZ%0A%2FQkAyrWUb9L59r7sQSuXrhIb7IwBbmZabsSBhLbQoCMxAoC9pLaBI8Cg6bTlhLiu0dx84P3ePU74%0AB4tMhlAst1qJ37xOaBQIEKF2TxdVigjkX561MSkSvY3ix5m4jXr7OwIGq50AN%2BuyQAtLdxbenoNk%0A|预订|55000000G602|G6|SHH|VNP|SHH|VNP|07:00|11:36|04:36|Y|5PC2TQRSdJGBdQpT0PLHJ%2BsfsGiBi7v8uuGj8935q7nKYh0q|20210509|3|H1|01|05|1|0|||||||||||有|有|无||O0M090|OM9|0|1||O060400021M1012500219201300000|0|||||1|#1#Q03|', 'AsCfVUZetegXeXyKf6gltYCDiIpz%2FGNZCMughy%2BlFOuu2QAZmjRQaamR3SM2XER98LFwXNqdJ300%0At2oEjfX4wvy2LEhf46eZj3w097oSpQyKxSdItHx537URpFaP2%2FGQE42sfp4WBJQZgaqfplTMpoM7%0AqVNL5Y%2B5IviKM56BB9knqzR6VhgkOAtikaT548dBmD6yrbLnHtVCX6nw8y0ud4eun9iJMomgue%2Fl%0AR%2BNlX2m5Dl9GimuEUh1vzIq145JjlDxktAI%2FTFrn55JUNmaccFdoS77talaqzYGiUbPVGyVHQ8yt%0AuEqOBRpkePk%3D|预订|5l0000G106B2|G106|AOH|VNP|AOH|VNP|07:12|13:12|06:00|Y|%2B0FLNPGdHfBfzbZxqX9umr423BT4j6ShXc4JVUxCl2mdvl6y|20210509|3|HY|01|10|1|0|||||||||||有|有|13||O0M090|OM9|1|0||O052600021M0884000219174800013|0|||||1|#0#0|', 'EJ%2B6msn0%2BNGFv074r3DZfjYJ6G2qoHMICfspF6E77stdBrTUUZ2RSpTeZjgzq858EFIuXqDdOFHU%0A5yqilNkPqF%2BeBugpPh8lyiA33mnZtDoWaEeAminTjsHSN%2BHL3ywaL5L9foWGDKGuznwtRAnIOZkZ%0A4nuBmUv99rcM3dJFMMYD%2BLykUcmFeg9TliieciVdnD%2FXzak2Q8prUpxfvIAwH%2Bp8c6xzRkOJ4%2Btt%0AbFMuIv%2FTiFGSQPkMjC17pnwra0OnKCybdD83yYvP1UJsMjgaM6Q1S1CzXNs1cl74%2FisFMv5vjFKl%0AQQoMfCuBTOk%3D|预订|5l0000G10883|G108|AOH|VNP|AOH|VNP|07:22|13:22|06:00|Y|Mn26GQ899juj4DjL6LdrzobCbTTabXdk%2FJ4B6TS9J8FD7FT%2B|20210509|3|HY|01|12|1|0|||||||||||有|有|5||O0M090|OM9|1|0||O052500021M0884000219174800005|0|||||1|#1#0|', 'GDUzvDldwgDgtmPm62zQWtUWuIkIlJq%2F2V%2BM8XYAf4UT%2BfsP7VD5uUakZeD2JQ3NvA8Gtr%2B2JtrQ%0ALXE5QwTauU1a%2BrxEHF%2BBXgv8rcIoCZxV%2FgoRtfcHi35GzAPQxS%2FqfxbEjdgUlKxUOqZRu4B0XOmh%0A9smplPNERhr%2BYnS9KcQh%2BYQ%2F2RyeVMgGDhSdTLPNTvm%2Fs%2Fr3jJBUXKYUpnrOT%2B9wTlFyhB3Lt%2BgB%0ArWUh4BBT6HuyTPv%2FayM96tElMMxLkYwYpV66RoGkzgUPwqU2%2FGgFXGO%2BlR9RUtxGztxwFDdQbGZh%0AHEwIs0bKdX8%3D|预订|5q0000G11002|G110|EPH|VNP|AOH|VNP|07:28|13:38|06:10|Y|%2FYQ0DGUY2iu9H%2Faatn5731iQMCIhoildJPGRHfLDDd52XyP5|20210509|3|HY|02|12|1|0|||||||||||有|有|1||O0M090|OM9|1|0||O052600021M0884000219174800001|0|||||1|#1#0|', 'xSlGphIaKibXNk%2BTO8g%2FK0IwmxCVS3Z2gWS%2FimMpx%2BQInAhB2XWChGgk2hfDfkQTUJ8yRd4h5Wc0%0AgGOD%2FwG6c2d3bRL1tBSn0ZsdahvQWg3mfuLg79Nf8jnsKzw2mllLvgKeu%2FW%2FPjtyu7wBivCtKuoD%0A4BOQ%2BA9i0pjDJRNSnLgKa5%2F9lx2IMyl73njTsgQodKbig70WslQ9BQZb1pWYFI6ebImxsKdNTjXD%0AQFoWixkqSsHEQKlq3tdXX4a2GuyCL%2B7MBxIh047W9muZ1DUDOzGlqQkxhTD6wMIQEJry6TlkXXbu%0AtR9QuGFHel8%3D|预订|5l0000G120S1|G120|AOH|VNP|AOH|VNP|07:45|13:33|05:48|Y|LnPZgQ9mzj%2Be5OhbJSNKvkJ3uhF7y19FJeOpKdI2c4WYcEqt|20210509|3|H6|01|08|1|0|||||||||||有|有|6||O0M090|OM9|1|0||O055300021M0930000219174800006|0|||||1|#1#0|', 'iuIB54dyVGJgVUToiCWCWG00nAbZrCZzBwrwx6ML%2F%2FuR8k86lHIpLns4em8ZoKjDH0BC8ZmXWcpw%0AA%2FO9fv4NCXROrGdvS4VV%2F2OjHm9ZXL3H0vvHW3LjslIvvPC5FVQpqvA9SaeDQ8Hy8xQ8wUYrZEsk%0A%2BtQ8n25hQzhMmoD2MCchs3r2QXCwnictxcawZR0BduWey74mU5EavSSotObhDc1BmlaarJ6b1twb%0AU8okxoBcJzx3PihYXwFd6IkfTbdhIEsKJYefECIv0O07l94fQ8L%2FZwIW90G5ldS79cnzP6fzsrxQ%0AcV%2F%2F1A%3D%3D|预订|5l000000G816|G8|AOH|VNP|AOH|VNP|08:00|12:24|04:24|Y|dZQ1JSLU0YBuvkCM%2F9m%2B2YDMqZcb7C1ZSI3%2FHClsJK0SW1mP|20210509|3|H6|01|04|1|0|||||||||||有|有|1||O0M090|OM9|0|0||O059800021M1006000219199800001|0|||||1|#1#0|', 'iMQwGy3JqaFPApjuwSH2dMZO%2Fb2V6C5FNZlGvtlJ74Uk1qYkTjI5DmGXc8svhEoHP7Qqd0hv6I8n%0AHx3qtAqCVSAXKY2IzXXRAvSIfPqoOx4J8qena%2FzAb8nwEBToZ9D6uaBFb8sS2YCb5y%2BbB6TN36tp%0ASFebAVrH%2BKkq1x2X4tahE%2FbTScvTz4h8fuaLtlYU%2F5wQabRp0VUihxOYYYNkOsZTdPpxNufHh2vi%0A7ffEXajyO%2BFurLtpDEdbnySg2OcZP0iJlz%2FZOCOxKp80GZNEdsWSDk5XN4Ypi53laeZLTkWcRB5M%0Ab8D9JxoOmu0%3D|预订|5l0000G11299|G112|AOH|VNP|AOH|VNP|08:05|14:08|06:03|Y|96AnpmpQ8%2FXLl4bDD1ilHo8NKSiZnkNChH38mGHQx8y8RB0n|20210509|3|HY|01|11|1|0|||||||||||有|有|3||O0M090|OM9|0|0||O055300021M0930000219187300003|0|||||1|#1#0|', 'RRYGLfAbaqWY61LK4UKPYdfe2k%2FHvWEyx4PiolxdvHnVAEIwqSYlzBkJb0LPud8zByzjiLEfvVOO%0A8HIUlKn4vrPLvebb8R%2FLNBGQrvO5VryIVXbyUNd9HFbk2xHMHu8i3jYA7yJ1G95SUYw0%2BxoBDIEL%0AGDvdMIq%2FKLKuFSGEVUJhL8DNfQ0kjmmKZ4%2BiB4f1dPrr8dHvvWW5pBxJQi91OTXuyFCuoQlFWO9f%0AjmstEY5L0wXbhpAqO2AWoxd%2FdItoCQjGgWzqhwYYvMryI4Own1PHhzlAm23DiEGTEuqwx%2B7LCLqE%0AjX%2BM1TmyLw4%3D|预订|5l0000G11491|G114|AOH|VNP|AOH|VNP|08:15|14:13|05:58|Y|nZ%2Fim%2B0BcVpA5xbVum5aa9tObmK%2ByKtV2GCDVSXShiVEF3MY|20210509|3|HY|01|11|1|0|||||||||||有|无|1||O0M090|OM9|0|1||O055300021M0930000009174800001|0|||||1|0#1#0|', 'kJILwouZkm1Ktx%2Ftr5%2BugdEiIA2K8vXpRPH7l%2BdmjPriLzwgnGnlTezLUpr3iq8TbHCBPGazSfgl%0AZ8mnKTkftXp%2BK82f00sy5INcUPyyBbbAU0B7Mlud6Gb10cDWfB3s7L2VfMzOFdoNQc5M4o5czI7Q%0AUONfOmsWu0XqDUwsoH%2Bt9y8SLot8m3Eza50Abu66dmshZwjGuThl6UG50C4IseqlqJQdTbN9xpLy%0AulccoSVDd5on1GzWJRxsk3%2BlLwuTqGYW%2BBBe8riyBzOIIeAbfAJr3ZObaWhmsn9oZiMf7XdQxfEo%0AwZ2m7qA%2BRAs%3D|预订|5l000000G241|G2|AOH|VNP|AOH|VNP|09:00|13:28|04:28|Y|I6GqV0LjvEPWSXR9Ixkc8yQ4SN4z1NMAatr0%2B2V9DItN1s8U|20210509|3|HY|01|04|1|0|||||||||||有|有|无||O0M090|OM9|0|1||O059800021M1006000219199800000|0|||||1|#1#Q03|', 'Ck0Mxew%2Bn8cTOe1Z1sKFk5NOY507dYZOg%2FTl5jdtgDEC1jpxAiA%2FLvGGehQh8AeBWZxY5%2B9b65rV%0AMTOTlNc9nAU%2BhNtPEP4TWtEdWqqC880JGjCOAjZhIa4ONWZ34%2BVtcCKN5KagTYHXxVRFW3dirb3L%0AOwtFXYPEqgEmUv7wQxfoyUXbzzRZUEkgAItCi4CaUP08ik5FZ3%2FL7MSqsxhyb42ciUmZ1oy0uSG7%0AL16EqX5fV0htuswxzlSq4yjDwWkCWIeah3WCyvpYc72xxY893i32qPnjKejn2TIrAd2aeiKRXMiR%0AQJ%2FWdGo%2FoZo%3D|预订|5l0000G11683|G116|AOH|VNP|AOH|VNP|09:34|15:23|05:49|Y|i1vehNR17ls0sd1uKrWFH9hN8L4iUqok46f99Ov7ReqmTu9o|20210509|3|HY|01|10|1|0|||||||||||有|有|1||O0M090|OM9|0|0||O055300021M0930000219187300001|0|||||1|#1#0|', '3Td%2BYjsvrwCGLCjRyQAcg7GF0panhD5vZaub8N2fxrLfrqlzz9xYTLrdEJuX%2BZEmvXsCdjL%2FLbx7%0Af43vIOJUxNgs7%2FKstGU4tsCHlqzhe847asTouNXsyyxBGlDYUG4dkzfAjBmPuwWpo4LCAP1YkPko%0AYWyW0BRm%2F5k4kBtdjogCZ2fRipA2h641V6iZXiiglDJu6ALnpfULGvi5a8lWtl41P0VlMa62iTaX%0AVjBshqxhfgzdX8uRpJ5br21%2FxVLvAt9Ws1eMBndSiEoCN1aUB1va%2FXEb7YO%2BM2682GBkekY0TbX9%0AlE1WlPpCKbs%3D|预订|5l0000G12603|G126|AOH|VNP|AOH|VNP|09:52|15:58|06:06|Y|KamApUZvldZ9Q6mesE79wscCdqxOdNMQTwBfgl5qnCpvlpL9|20210509|3|H6|01|10|1|0|||||||||||有|有|1||O0M090|OM9|0|0||O055300021M0930000219174800001|0|||||1|#1#0|', 'OoDjHj%2F0YqwDawuVp9NInPibaC1oK7jPABBif%2FuiM6eKVeq%2F06b%2BWJpgGyI%2FpBnmgI68MFjc%2Bq9S%0ANjPlRboyAZ0Visw7F1NfRbt3xVmAEV5vArzPWDq1ETrsl6d95KhdwyGFRli9w3b7yiya3RSHm%2FGo%0AkYuN2jDr04jmlOs2HrcKLkfSaBXaCZjKkpaXuAXkaSRzSWanB9DN02FrC%2FkV7aq4LlI2FfkdfGb5%0AN3Hv1ippWZvDCaqSqRWE8mtJI8uLi3pgUwiLol4EP0Oyg7MSlGYHsKlKGRQDSb%2F3JnHQ%2FR1w8edo%0A%2BcUMPCjkE2s%3D|预订|5l00000G1003|G10|AOH|VNP|AOH|VNP|10:00|14:28|04:28|Y|174G9itXjeHzOlHEhuOSZ%2BqpIyq4AZ%2FenIpB9A6oXHUXcemt|20210509|3|H1|01|04|1|0|||||||||||有|有|无||O0M090|OM9|0|1||O059800021M1006000219199800000|0|||||1|#1#0|', '9NMa%2F6O5Er8gH7f%2BSX3NigIZaGN4Z%2FQA4ewd7WLLCK%2FeymylWXFUHegLvGsCiCPB4Vide4IevrMC%0AcoGWEJTiAbPn0uRm6%2F%2F8F86ZJXjmlUfTOQ46DbFNPJVQ%2BVRZfCo7mIKyRh88SavLtLcWak0qdsPc%0Aq9Qh%2BF2DfOW9YiGLRwciDSKstae5Q7JB62XW86%2BAhLIcNhhaqtgDhrho3PYTtTt7kRfo%2FDD1ntYO%0Ab5FVpQKqRZseNxlVmSk4ffyNam1VOgF7frOip3SCRfjyOK9%2FpPWUA%2BsSnr0sdYxPgREXC58hHBt9%0AXfD89v%2BmHMI%3D|预订|5l0000G122E0|G122|AOH|VNP|AOH|VNP|10:40|16:43|06:03|Y|le7WvfaAOxDX4emj00sAdk4LxirE7ny3qHKlwINyko4sj43d|20210509|3|H6|01|11|1|0|||||||||||有|有|1||O0M090|OM9|0|0||O055200021M0930000219174800001|0|||||1|0#1#0|', '0XiDZFk8EtyvXZWtQtT8BY1IuyR9mQmajU4YrDcodJP6CLbrJPu77M6rotfiYiZ3ebe9KEDokOzj%0AMydwyZvTfUzOJUQbWJsv9kZLmH75lTnycqEk7Hi%2FgCnae6YxTqXlC%2BDMwnOu5cyxrr8hkVXhGe5p%0A8pgpVpk64Xu200P%2Bog7UYl%2B5gDWNtDdosy0iQcTLTutyJMdU5Sx6y8UaKw8bBMUcx%2BEQMMds0xW4%0AuLvCZ4tkiuH6HYQt2bF%2B2GHhYcivtkAi2AsPnjBsEd92d%2BFFaPfcixY%2FI%2FIlvEHR5XaziHQcF1JV%0Al44tR3zzgS4%3D|预订|5l0000G12403|G124|AOH|VNP|AOH|VNP|10:58|16:17|05:19|Y|o0T1Xv%2Fr%2BR933PXkPS0V5yet%2FvIqVIruuZ%2BnFUJw%2FpvTyilQ|20210509|3|H6|01|06|1|0|||||||||||有|有|3||O0M090|OM9|0|0||O057600021M0969000219199800003|0|||||1|#1#0|', 't5WI1TstybUyTXhJpg%2BbiP6fkk09wTDQZtQGldO3kn%2B3YuGBLHdi8y7VOct60ae5zNiMV%2FNM782N%0AVFcRWuCqn3Ddwl8rg4IBE6IBPl8sF517q%2FrkrrrxLZiYx%2FJ2MDmgzA4FDsOGy6s7L3kn%2BoXVtQtm%0Az8Jc0z7%2FvATVMoS06n7EeUlxd3RYkixRGvVIEHt6PjivQtAr0gAfgaQk4BOamng2p3vlcGabIElB%0AQYbYJB7rB%2F7BRk0vqwsrTF9Q3zgVpbdU7Xrn3FLv2%2FZCtzvY3u%2FNKhT2H0mIQcoqXANlXp2MoNLI%0A|预订|550000G13011|G130|SHH|VNP|SHH|VNP|11:15|17:44|06:29|Y|U5L4258F%2BCdN08aas218XPKJvETJzw4HR2dzRAI3Pl4D2uAw|20210509|3|H1|01|14|1|0|||||||||||有|1|1||O0M090|OM9|0|0||O055800021M0937500019188900001|0|||||1|#0#0|', 'mZfGexv0MTBqjQKuJfidH0b5J1mu8akEEOkseqgUAODukcGQ8BgT974ev9d8WLJQ1FrNyfQZE2p8%0ArtTvBTzBJziPUOl67vtiC1vMAnH35lx7MesaDhCN27OAHr%2BXMsHWkZQwlFaOj4LLdcpkGxJhp1vI%0AI14bWjBVkucTAu0KQYVibycgGuhu8sSqLwYbqreahipFN7yqlAPX1AJqKSaCDy8dbpYAhYFkt1FL%0AyShJP4K98juN986Q5aG6p1hrmg0L%2B1Hs38NRlPr%2BeKb1O0P3UT08DfCPWL%2FnTMwPbeM8Pn8QXTUo%0ALoUB%2Bw%3D%3D|预订|5500000G1203|G12|SHH|VNP|SHH|VNP|11:53|16:38|04:45|Y|%2Bm0lxaFs3KwwJ7K8gfS%2BrmheFwhNZTOFskTStiFHPeZTgnG5|20210509|3|H1|01|05|1|0|||||||||||有|有|无||O0M090|OM9|0|1|O|O060400021M1012500219201300000|0|||||1|#1#Q03|', 'C6j4iuiaFeQUzae1VRQkndaYr69dvNUw1cSqcRqu85GYH2BeRCyimD1UvZexp8vQ%2Bj%2BFBTl7%2BrcK%0A8vyPJGxt4Xh0QCwZkZHfYOQ%2BPiwyz1lQ0k0YdPYf8MrTDEcqJOtP2T26mb9ExNfPApCUm7wFoMZl%0AQ%2FG5iDa9lfkgM0wLvtEz0%2BofptKoLrhrwHTGbXdYSih0KzT%2BB1S6XBjncY%2FN6Q3A6ATRYkn038JI%0Ajpoo3Bg9pddQ23Xg%2BUAxazLSWIwDEmf3BleuPw%2Ff6%2FVCqrNU1ZNoGqO%2FM211mYnQ4GD7ztvyjoG0%0AYL9zzXXwesc%3D|预订|550000146202|1462|SHH|BJP|SHH|BJP|12:15|10:50|22:35|Y|1bx8n%2FdG2dgfvQCXhkk%2FB5vpT92JuCmzAfdz84TnU9t1sDQ3yZxfWROuX7I%3D|20210509|3|H2|01|23|1|0||||18|||无||有|有|||||304010W0|3411|0|0||3028350021404555001810156500211015653000|0|||||1|#0#0|', '9nCrdgOzA3%2F4oDW%2BkE5uEigxQVkK%2BZ%2BIm0jJ3lbiNkxNuBy1y1h7vYBBReD1MSQRha15%2FbswaAhE%0A17WUaN1m6cNi%2Bp6x6qciez5INMPAmx47o%2BuiFfBstg9bxv3xgYYxYlYfXgD3wlCDw8u%2B5ONBK4HB%0A3WrIPy1PyczqV2rYnr2UQxq3I32vK87%2FQXtRQ6a0XnWox9tA%2FTNpt2V7zO4dQ0lDf8G295VJe73W%0AFthxmA1b%2BzWmnKd0Ynvhl8OD%2FgcAjMhXnfKaNBr9Odbqn2Ar0FE%2BFidO1cTHQT05rOouXzM%2BJ3f4%0AO%2Fms7ymNVdA%3D|预订|5l0000G132F2|G132|AOH|VNP|AOH|VNP|12:17|18:32|06:15|Y|4EzsnHnZeSXZasItG8HFBiE4KFT9ablNK86MU7dFvd8OF%2Fmy|20210509|3|H1|01|12|1|0|||||||||||有|无|无||O0M090|OM9|0|1||O055300021M0930000009187300000|0|||||1|#1#0|', 'oO8%2Ft5YOhbT5wBaNdijOZmKNYOt1aibW%2FndfXQ1nvzV53iVGTXAJldm0mBHIEAv%2B83xlqidUuKrQ%0AhtfDXqfzEBIsbP3sUWYnPwtNXmfU%2BEWXlg6a6NTJEl%2FkAIdEyV9ywbe6xnDdoxr41jvegIWtFZBd%0AuBvUDaD2IDrp9UldBmniW5%2BXcetBuNEEutNYk%2BRZL4b87cVsuBiSYt1yfjzjSbKF0LozTOn3s5%2BA%0AtTvqF8qD56LZponvoolXmlorRAZ2PZoPZ5sefN7trgE0z%2B2zLwKjdg2ARdooePx1YKgK0BxGb%2FTB%0AaH0xPTJDWak%3D|预订|5l0000G41271|G412|AOH|VNP|AOH|VNP|12:28|18:58|06:30|Y|kniZXAMjEra8tp8YvPBbp%2F9XOKDTVEkxnVz4HWulZ0bc36lW|20210509|3|H2|01|10|1|0|||||||||||有|有|4||O0M090|OM9|0|0||O052400021M0884000219174800004|0|||||1|#0#0|', 'RLzS4elix2Cdq1mBwA0BKVu1UMn8Vx6CVtciuxNXyjR2OeR2JOf22qGMJcNNoRwnMTH4RX5YcqXH%0A3%2BHiOw%2F52%2FSK0UxD5G7ejTZX6J8kGYxKZcS8pU6JjTWLwqy923Pz%2BdmdfCZPtNYEkG1jJdrgJ4%2Bp%0AxSRZO23d%2Fa3w4%2F%2BLuLPhxPXIoGvD8ADk58bfhzSz1ghxPl%2B1CT54BZev8lWUNyw4eahlLJ6FcTkn%0AotmWHoHUHCmRQFAMfQPXq8KJBDrgd0r8D2ByQ5qbo5L4Z596kCz2seO1%2BuYt4RvfuIw%2BsUIsdOLK%0A%2FNx%2BBZVsTwI%3D|预订|5l0000G134B2|G134|AOH|VNP|AOH|VNP|13:00|18:48|05:48|Y|GEBU%2FiF1hk%2BupO%2BS8yoA5Y9dvVFvw1SksEUv3SlzBcyAoE7r|20210509|3|H6|01|09|1|0|||||||||||有|有|无||O0M090|OM9|0|1||O057600021M0969000219199800000|0|||||1|#1#0|', 'vDMYAVcEkUCMinI6uCBCyhQQ6Ul3%2B%2FlWC4177y%2FGyKUeCk6ENrrz8w2%2BdHNK9HqSt%2B9iqZ%2Bv%2BGFE%0A0PJQizMJBt%2Br4YVkoSbFmuL%2FQ3uH5eHs%2FOfhiviR0sXWYZHbaQ449LI8sZwYTZRtKTyBFVQ%2BGuI4%0AB6guU4byuKJCY6YYvkHtCt6%2FyknLgmrkp4KRWSidNsANOmESThD4niVBzkl3yA0V75mbjTflqII0%0A4RXQiLaBmtYliBU4S6ExG8nh67tf%2FE9kMLV7%2F6ZdV5W2Bp5XTOYgvpmVgVz%2FaIVp6yUwogUEGTs1%0AO%2FkDQDOqXzs%3D|预订|5l0000G13863|G138|AOH|VNP|AOH|VNP|13:29|19:26|05:57|Y|9rtXhgFdi3IijpWqt%2B22Lc%2BY39mJaAamHLpxPfR1P4VonZHV|20210509|3|H6|01|12|1|0|||||||||||有|有|6||O0M090|OM9|0|0||O057600021M0969000219199800006|0|||||1|#1#0|', 'bIPsjpgZizCf%2FVq%2BV%2FV7fYoI%2BWxlNvAJW12CzeUJnb3bS7JMavW48ANK4l935meR3WRYX50YWHOn%0AzSRYxggMtB7WhHEm1Vs0gQPMUvpPoL2jyGnq4xb9EcyRqvox%2BibgEkXsv0iRYlMepsz2XyDuRhDT%0AvQhn2ylcdwrSyA5LKj8dBvx1NlojGCJaw6a8nL%2BkJ%2BuSlSlG07CJC08xFSqJ8KgEvL2lN2MZjTqA%0AVHCD%2F7BC7%2Fek6I42mQUeICcrRHg4cvY3ZHj6Y0PkeEW9JAs7kNpmG5uNKZwct6EvsOoscsWl6ta%2B%0A%2B%2FIk%2Fq98Eqs%3D|预订|5l0000G14071|G140|AOH|VNP|AOH|VNP|13:34|19:40|06:06|Y|UBy52DEETzsAOs7OgEX2Ng381MdmNA7CI3P8YEzZZK5tMnuH|20210509|3|H6|01|11|1|0|||||||||||有|有|7||O0M090|OM9|0|0||O055300021M0930000219174800007|0|||||1|0#0#0|', '0ZwnijV5pS22Et99XoO8q2xGjEIATX3wOsoMhqBXzLiHebb49F6LvpG6%2B3tLijmAREHYiEg3TStg%0A3Pt7C%2FthYKYg7Y4du5P5vquTthzDO76tJ1u1HtmluQYVqlc8Bn9lIvAbJRMISgOUvExiWAqojrI6%0AREvQRB%2BEO4hAeDPt0Y2jDuwJWJgL0S%2FeRiQjXSxB4mjlAyjQ4Xi6NyCfwRXkNuRXdBVIPcJOTYdQ%0AZQpWyNAI7oqtQZE2Dma56OUcqoOqviFgcLWEXnIqU54PbSMnAQ6DoT13%2Fcu8wTMMR9GOy3qhYT9q%0AXyWg0efUYGg%3D|预订|5l000000G440|G4|AOH|VNP|AOH|VNP|14:00|18:28|04:28|Y|Cn83eV2%2FuyZ5J32z4aI7I9K5qV4e%2B2BqVCzbSnBMBReJwf6D|20210509|3|H6|01|04|1|0|||||||||||有|有|无||O0M090|OM9|0|1||O059800021M1006000219199800000|0|||||1|#1#Q03|', '0UmJwsou%2FnZVR9sknD%2BPW0dHufXzZ3UNECCe%2FPHOlGbml9Z%2B%2F4kwARMvm%2B3ZVEf5PPkuwtQsIPHa%0Aem61GFbLZpmSWgmB%2BFMF1fcwGWNOb%2FZ%2Bv3X2vQC%2FbMeIc9vIaOEBm35Vf9ZXca2hIWq230Y9BVzO%0A3xID%2BvI%2B213dM4aF%2FVmjt3vW2vcanLrz2KWAyMz4%2FXdhwf3ma3rYif8DjY%2FuJuNLAKlY1Wqa61Qy%0AX9sg3B2s76p0FctPFsDb0dhnQK1LDiCs6vL2iaWTz7Ja7Lfjk7s%2BCemMJFfTLjwXBPogMjmKVWZO%0AXK9oIn9JMdQ%3D|预订|5l0000G14263|G142|AOH|VNP|AOH|VNP|14:10|20:29|06:19|Y|VOJINapiIPxp4Nxg2UIZrlZKKQrdlOFLLogxX90y%2F5hUm6F%2B|20210509|3|H6|01|11|1|0|||||||||||有|有|16||O0M090|OM9|0|0||O055300021M0930000219174800016|0|||||1|#0#0|', 'fFS86qAxnbZdH0hBJ2qiNrndJKpbYvIPkQ97hRSZyTkTx0zH9jSPUj6KvoDNNqlF3O2La6sclqeh%0AO5BukZU06eLuomZISK9fssARcH9LI8zVS9YfR%2FJ4tnWnwGoupzvk7v3GV070R8P7rIhGnkw%2BARpt%0A5zKD1lqDtePVShG9%2B7M1drU%2FNOTnBukxI6kEr47olXjz1ZkvG7Cowzuw%2FvQOwJzRNmhkzYpBPFkV%0AMentanjmcSoI9%2FoMTcQZkkqwaC5GdWrspdO%2F1Xj4mYWwRqN2gierkbVTRrXtOPerr2UMRNjqfYQ3%0AsPTWRMR67ow%3D|预订|5l0000G14604|G146|AOH|VNP|AOH|VNP|14:50|20:48|05:58|Y|%2FcOOb8XSqS8knYcMWojvefje0imLMXxNA2qHBGOA%2BdTkw0KB|20210509|3|H6|01|10|1|0|||||||||||有|无|无||O0M090|OM9|0|1||O055300021M0930000009187300000|0|||||1|#1#0|', 'KBvMAJ%2FfuO%2F%2FQQtDZsrfTeu%2F38G40WnEKdSzReJ8XvH0YNp0uasp2mcOtRgp7zHRp4WR7nAEzTPs%0AlmVmoUf3Nwq%2F709ch0w1xVrKk5yBYfmgC7kxFDCxV%2FkUvW6b%2BYTDhyzKPo9MybHGNSn9xVE%2F1MIa%0A81yKCY58SzgmFWFmkA14c26FaD7BPSCeK%2BZZ%2Bk9%2BO9haZqH7zkq8nUhhrb1cboZ%2FZZxNG9YMA3jO%0AJsQifcRFToBbb%2Fe2W6mDQxWvepoVlCWgdhBy%2BECD2KbouS1KphLsFc0340olLAhboCHQ684JI7zQ%0ApTcIzcuroGY%3D|预订|5l00000G1445|G14|AOH|VNP|AOH|VNP|15:00|19:35|04:35|Y|f8ikhMRrjWQk8gdwnAnDttZkYk9pAYX8GgWOLnoNLF72M1%2FP|20210509|3|H6|01|05|1|0|||||||||||有|有|无||O0M090|OM9|0|1||O059800021M1006000219199800000|0|||||1|#1#0|', 'JAAGb81zeSNXEE6gj5f5lEdYqqMfX7DprkopMCMI%2FHAatoxsVzr7mjQ6d8cPlNvexavfkpAFJ0cZ%0AH18NJg4l0cB04%2BPYAPxaZC11HjlwtRnrhe98bpIpCqlL00srEVCl0JP%2FjjEGiKAKnWs6%2B1E5pLEm%0Apmnz1Gwid%2Bd5zwgMLcdYWyr5jLtP3xCUSKcWrz6t95k5CcZH9fQP5DQn1Doyjv%2F%2B9qwEtKXouLJG%0AdqUZlGWj%2FMxKoP126%2BYUbd4545gTqVP%2FYsjNbqyRPwZ%2BxmLfBIO%2FWor9FZjL%2FAAurjt6bNGyh7ad%0A8Dc%2BB96I3uU%3D|预订|5l0000G148E1|G148|AOH|VNP|AOH|VNP|15:22|21:13|05:51|Y|9f760ubkr%2BZ%2B965up8oaaKyK%2BeQY2jCA6ju9vSc%2FZGnmJ%2FG8|20210509|3|H6|01|10|1|0|||||||||||有|1|无||O0M090|OM9|0|1||O055300021M0930000019174800000|0|||||1|#1#0|', 'Cxm0tRvp1o939NShR49Q4CaLR24Ltq0HsAG%2BP6CMdEWfILw04wtLZRnBtRFIB3RgKQBeOUupxK6b%0Af%2BKRJKq%2BkyNSNt%2FneIemrBVjruyRCqdX%2FX%2BBmg7kpmOpBimgVU%2FpCF1BMSBDJW8yozafUrhIBK08%0AO%2BaKi2c9WZm8s0BrdCr0TfUKzMFZLGwa4N5UgnutHAP8BS1nu6KEtaW3YjvtmZ2TlwUgxN1FAzuL%0AWBiAMiypZc1xMizLPvbg%2Fw1%2FqbSEHWzunZcyqXH6J1EWFwoNZ6wGuMBbaTEQiuJB7ZKGEt4O6aPn%0ASDtTx4B1tqo%3D|预订|5l0000G17007|G170|AOH|VNP|AOH|VNP|15:52|21:18|05:26|Y|00AIIJpFBChBGBlhAP%2Bkg%2BDuduqN8WWGYuWkcGE3QBBjtVZC|20210509|3|H1|01|08|1|0|||||||||||有|无|无||O0M090|OM9|0|1||O055300021M0930000009174800000|0|||||1|#1#0|', 'ErH93%2FGuN819z6AdbY3Kb%2B1lSqvTXvzhwZKoSETiu6GcUJwC7blv1E19FMyfph4%2F0Hg4ouD8Glyt%0ATrhMZWBjImMvv9Gupg1N1H2mKgXSdYNqbVG7Hr7f9hZys42Iss%2F0GX337giW9%2F4CFmxQ3NFlC%2F%2Fl%0AYaCBs6w2VjRixFYVwBiKN87jGlNJBasXwUBUzlXFQQFhRLPDwaeF6309TCxSjVh6MOpki5Vn0Bs%2F%0AVJAC6MJGUQW4MdyRxBcVSl7gOnrGv7ehwDyWtws83BWmxivDIq3PsQfuMvhh9US3ByX3qCCkcyWJ%0AnbEtLtpX4ko%3D|预订|5l0000G15007|G150|AOH|VNP|AOH|VNP|16:07|22:00|05:53|Y|tTpcsIvIuq2FrXSnyRloHoD%2BFgxSMq%2BXXs%2FkOZyHaS8ZPzvx|20210509|3|H6|01|10|1|0|||||||||||有|有|1||O0M090|OM9|0|0||O055100021M0930000219174800001|0|||||1|#1#0|', 'dAwazlbiqhaPDYkdxyp4%2B7Y5LBGJlS5tKeJvQbJ2raIuCsuqaGcSsrmi9H9fW94kXA%2BGIdPYiouN%0Az5MUt8di69obiuToNX6HfoLIpVa9iEEj0MN6suiGfxuZzH2dtsQR%2B6XU%2FNzip%2BLAUVdVoSMS7T72%0Azt3sKjFWNxV4Lkkyn5CLUEy1MNLabpzcUG%2F2c9hkk2s5RtReHTGsdEzV1UWPrT2tvhwX2TUqgZeX%0A1H0PrNj3TWbhggxAX22mDUmg0Afrk9NtC%2F5fk4WGv0T0%2BXyQpuwlD3OoS1bflOAMP8CTQYpLAAld%0ACTGpdeSj3mA%3D|预订|5l0000G152E0|G152|AOH|VNP|AOH|VNP|16:18|22:12|05:54|Y|Cgxwk4BJrGd8nDbcOjI827QD%2Bs0h%2B7zok66G1vdN%2BrQrJWz4|20210509|3|H6|01|10|1|0|||||||||||有|2|5||O0M090|OM9|0|0||O055300021M0930000029174800005|0|||||1|#0#0|', 'uCAB6vVt8zLQTYeaaLoiMVsjokzXoDry5OiQKiU2RyxLYWBrkk4mkekxGAI8TUHS%2FhrY4Y1X1EEl%0A%2FH5s5s11yVjlDg5Ap6ZesoCF3NNhdjFTRVK%2FFvN2Cqr0neYC9IfP6hy2h%2FqEe1SikN8I%2BinVS11H%0A7abDqpA%2FnxjmFDwn9NI6c9j8rcqRaccegOWYjgY6907U1x%2FX%2FQmWWb9cffC4RkH%2BgaEU7quEbKGE%0AdVsD7Mlt%2BtGnJin%2FC0ER0HxDeY1kixWFWSGC6sVFNI931CRq026NOioTB7%2F01N34nhlk4jtLrV6s%0AHrdzGIT00yI%3D|预订|5l00000G1614|G16|AOH|VNP|AOH|VNP|17:00|21:36|04:36|Y|8TFm29VBH5R782IyzHRzk%2BJnI32NA7t56eUZ9EFPXBxU3P2e|20210509|3|H6|01|05|1|0|||||||||||有|有|无||O0M090|OM9|0|1||O059800021M1006000219199800000|0|||||1|#1#Q03|', 'qLEGD3LjKM5XKCx0XxZUYtn7TMWhM%2BtXoyQm3KO9Nu8U4cIZB093tUVUvBrml0h7soGRSogZpImo%0AMrVZh82fj8UGTPvpfwv6aNy47b5jjXq19BenIc%2FN%2BunoDNnM8WRlOpw%2Fht1rG2kJwGXmtMn29fLC%0Ag6IDEKYVplw3McfmuLgIIFWD8jnqa%2BJ1e%2FFheLzi3O7owky%2FHkBlDN4jRe8C%2F7JvO9F7NBZ3wvhS%0AznpaKuk4chAmOCb0bFfbS0iO%2FbWyL9v3i9SxfOb5UDsCeDQdbJxmP4LtlpDkVM%2BT8FD1pFEHK0Gr%0AfzlbXnvIURQ%3D|预订|5l0000G15400|G154|AOH|VNP|AOH|VNP|17:13|22:53|05:40|Y|LeNtkvpzOk6vhq8InhIOwG7ii%2B%2B5EkxQePMosH1h%2FJoVJO7%2B|20210509|3|H6|01|08|1|0|||||||||||有|有|1||O0M090|OM9|0|0||O052400021M0884000219174800001|0|||||1|#1#0|', '8PSMEMKHUjJmAV9qdfDCSdlZ2Cbh5OwxJv%2F6zziYESPBsIO0R6yxpCnaa2Yh582hFnGpowM%2FlMfo%0AT49ZVMun6YmJD%2BHSTk%2FgNownWwQ8ZyMMfY3%2BVr0JmT%2Fsd9lCtHQvayQqTnOyn8uf6VI8bY%2FaoJT5%0Am4rsF6xt6VOEQy0qHY3Jahrzh0k7pfoufg0tBQhaiLPqF7t9izsVsGhMYnYqk1b5CpSrJ9UBQgSQ%0A%2F0PDexyTh5Eg%2FaI4%2FZW3LGFqaimBX2o2jWVrrbnkSd7NMMfTAwVO1pRMP5wbf15FvXiRKSJ9VVsd%0A3UoZsenx8D0%3D|预订|5l0000G15605|G156|AOH|VNP|AOH|VNP|17:18|23:07|05:49|Y|WDYcrS76P4J3GOoNaaTfnNCdE17B8E3n10toIFTekli01Rrw|20210509|3|H6|01|09|1|0|||||||||||有|有|7||O0M090|OM9|0|0||O052600021M0884000219174800007|0|||||1|#1#0|', '267NeyzU%2FAx80oTnxXAiWlezSUdLKD3%2FP6%2BBLj7djdfawrMYgYak7Z%2F90R12ozPFFC8jUiwv0%2Fit%0A9vG8RCdM62OHB%2FeRfXSp4Xwr0T4M3q9rhRFXP%2Fa%2F%2BIKO8QHvJAsvEh5R%2FtPspDLgaoTESvlIalMp%0AezvadkhfzBcyegAZ4f9ES9V0QWYaTDlxLRyxDhD881CHAyKMD6raaUAa2EmpNVzIkuxQiVG7vgO8%0AV4F%2BP2vUF8w4r9sqlucsAbjyBQotg9CWDmSrjZtarnIHVS4tBaBbXrZfUP8x7MMNjADHImK4rbqK%0A3lEhPd%2Fvonc%3D|预订|5600000G4401|G44|HGH|VNP|AOH|VNP|17:23|23:12|05:49|Y|nEdv1zED8hzJBRo1WpfuUO6E8eR9IMQmSPedHnC%2BHIOgqvd1|20210509|3|H6|04|13|1|0|||||||||||有|9|无||O0M090|OM9|0|1||O055100021M0930000099187300000|0|||||1|#1#0|', 'b0wQbsXQ4%2BGJyLIZlcgNY1Z0Ow5Wz9OahRVZTZkZmu4FBOMErSY%2FHGRDOe3MWOqZMt80LORNIwCz%0Ap2wQemDlWB3M6jMksYAXnSkLhOg6mWxrOM5JM7wflhzlr9ZYc5wrofaa1UHdiephWQK0UvFFrvQl%0AATcWT9cSRj6Dd6bgTXZuNEs6gxaw2Lu7aCcjGw%2FEHHIZivxGrjjwfMF3MwcMUrvrIEAQrW8twqdJ%0Ac%2Bp2WQyr9J2wj4WfEzSqWBU9pcZuQsVex1PQaKBx%2FYi%2F8tF3OMsShAqrfk%2FfGcfkew9Y9DEwjDvG%0Az6gWCfKEcbw%3D|预订|5l0000G158D3|G158|AOH|VNP|AOH|VNP|17:34|23:29|05:55|Y|gop4ezf7uI8JUD9hQf6sIFHqcBS%2F%2BDHygYmhc1dMVVHnjstE|20210509|3|H6|01|10|1|0|||||||||||有|有|8||O0M090|OM9|0|0||O049800021M0837000219174800008|0|||||1|#1#0|', 'ueFEF7ewoTK%2FSNXosStITKIrpXUmOYTa9wdcRc5W76xEq1OSj1gaMRH2JsO21oBSOvKoinY0Nxem%0A2lW2QmiunsTKczSgMpXjccfigZwdVHR%2FL3q05HIlxJmcMJbWVypbMxdlZPbxYfTvOEuh9l9V%2FIxj%0Ai2DTT22W8XMnJiE3baf34gOZxJwjOC6uGwa6jWe46UC06hICTV3gNSucq6bcfIptJ2U5nso7TS8U%0ARHNJcRJJe5j1GyfTaDkQPtU1HRF%2FWmvI0agGekwCq0XSkp%2FOchSKea6h6PmQgVKEAuuctnFzKnn8%0A|预订|5500000G1810|G18|SHH|VNP|SHH|VNP|17:55|22:36|04:41|Y|MI5r5O0SZOycE%2BjtYxsZTH8DZKaTywoj67cKqG4xIaNG2O6M|20210509|3|H6|01|05|1|0|||||||||||有|有|6||O0M090|OM9|0|0||O060400021M1012500219201300006|0|||||1|0#1#0|', '5M%2FdCrCB8VYBVjARlzvx6HY9L5gnQQokaMc48ZRcVEmiqoE675mMJEg7mFZIF4hukQ13tgKCOWNC%0AmAci0z3ODZrtCa6y94g1Vvewwbrznfu0lumIcgdrbsjyG%2B6d9R0KlXZtGz9%2F5kjBeOtPusKt089u%0AhVTRjGhoGsIOcwuawiy42IEQ1XhEgxy9UPlb1ZG6XTGByx8rWC4t9hm36jkQHz2YygP1a3tRpxdO%0At0oi6NUHldUpuQl4MV7%2BGuzbdzWF1aK9NblUgyFVWuLt6wqS3DrJEQ59XiDeY7392m%2BK7RQ1Y1os%0AyTH6HXvfO94%3D|预订|550000T11063|T110|SHH|BJP|SHH|BJP|17:57|10:08|16:11|Y|%2BpgydeccOjqlku%2B%2Fsct0Dp5d9ednFYTfjrk2xc6pwi91O21WI%2BSBcOaAs1o%3D|20210509|3|H3|01|10|1|0||||15|||无||有|有|||||304010W0|3411|0|0||3030450021404765001510177500211017753000|0|||||1|0#0#0|', '9NTjI3uVZxWk1e0InaBmgc%2BfuX9AzwA80u83ru31j0RmHCkfygH78RO4PifKzpLGYigIxFjDLNlx%0ABYXEixWRbGtFfoMk8h6o95mjWTuN3nfjHbvTAoqmGFIwlOrii0OKs9QfRTELcr%2FmglM1L8NGtfsY%0AWdEAiAj3bF%2BLWpW9d1f8TX54HS70B83fcF6M0XSyB3I7OfPBwPLIJpnH5vdkxtz%2Flar3HS7pvbsu%0AvhcxU%2F3nlD3Ia4%2B5h4BNTAZNVh5JfPM98Bk8Vl6437v4YEAbJqvt3tDNXzQFORSRAyER2IlFfrmC%0AlE%2B4nqDYTLQ%3D|预订|5l00000G221B|G22|AOH|VNP|AOH|VNP|19:00|23:18|04:18|Y|cjp0CU5cXTh2UxHre0um0grWAwvmj1cDbTJYCcK0lb8nP45d|20210509|3|H6|01|03|1|0|||||||||||有|有|1||O0M090|OM9|0|0||O059800021M1006000219199800001|0|||||1|#1#Q03|O059800021', 'OqfeyAsEH%2FEgY82lbzR7f8eherxb881ob4OvpKa0uDg7L8cLlKlWfNt88c0kVb4xdbv4icI2F5QP%0A8LwHkaAc0qQ5MVtoQkuXdPtZQNJDMIG1H%2BXafSka5Qap4QLUY34wOY%2B%2BpbGJOSpr%2FiGY8eo67nqQ%0A66y4pozUy6ZZF%2Fa9ks%2BJKObuD2C7Mdymm%2Bc38SEUbUempiEpEF9rv0zj2IDKxtzoeajy6IqoWwi1%0AhiFMeDdVvvqZUHLatQKvkQWyeQ3tfgIW0A5c4XEdYJbUoHecx7yx9B6p%2F7jMQgn7xWeV8MoR%2Bn%2BL%0AfWD05CMxdJw%3D|预订|550000D70200|D702|SHH|BJP|SHH|BJP|19:08|07:12|12:04|Y|k7dprjGMIS9rSvjLDotTeuxO9K57uNNOYrHZ3yJMETucy%2FKNX950GgMWjKo%3D|20210509|3|H6|01|05|1|0||||有|||有||有||有||||J0I0O0W0|JIOO|0|0||J037200021I047200021O024800021O024803029|0|||||1|#1#0|', 'qdjUYoqYjS4UqkbAu0OIgVM07l7G9VfoTaCCu1pPZz3MWFJ5KLgzRiUGPX6ps%2FaZfrU7gS0c5btX%0Aand49MKE25g2CBAKZh4vmdKt8NjDPuUS%2FOgHe%2FU61vGoF7fgQnsr6uJ%2Fh24k%2BwRM6MLp%2B%2BAGhjqS%0AVQhVFfGmDquA7Uzy8cD0ya4aLxq0ssjtQ9WjvJK97qhNwEtocAtRaUAu1p%2FX81DIslAAMCVAULPB%0Ajc1tKzi3lKKIn6gJD%2B2%2BwwjRUvjql1YLx37YGZlEUo%2BZpbN7FuEOSl20p9xdiyfs8u4hQM79MbHr%0AeulXYd8XnKsz4UMM|预订|560000Z28201|Z282|HZH|BTC|SNH|BJP|19:29|10:22|14:53|Y|EKv8pUlfBL%2BYKmcUuAV2OeusoUj0Y4HqmrPoFy3h9MvZKz2lNYlcJK0BEdY%3D|20210509|3|H6|04|16|1|0||||无|||无||无|有|||||304010W0|3411|0|1||3030450000404765000010177500211017753000|0|||||1|#0#0|', 'IWVjE3Kzh9tiSJVX7kIWKt%2FWv9zcApWK%2BLSsF75Vh3aJBo2s0j9g%2FhkK99b9gmL3Yi3dbnDw8KMT%0AeqpWVdCCVdUjoRN2LrWPnKUdwUTYFYpTJV8SlN6HNFp%2B6kx%2F6e2cFET0NLEtqJj4Wc%2BTanPrNopk%0Ah6VUMPTnVjEedBCM%2B9PV9lsJkpZbgiHaWlniKVmAQ69pEO%2FxVLJNtSuFTVt3d6SEZjo0%2BM08ByIE%0AE1qvJl%2FZGuF%2BwCmaqxodoOgaqJf15KtWcJYGU73mkLUhECBuWcEGdYnE%2FPlTUVlXVPledO%2BiCbUE%0AAgWRkZSBB7CRlqun%2FYNXwg%3D%3D|预订|5l0000D70600|D706|AOH|BJP|AOH|BJP|21:18|09:24|12:06|Y|Z%2F7nQyK21Vlt6hJFEr67epEjyd5w9DFmFpT80lk7EJsG3KuPkiLU9UVTn9o%3D|20210509|3|H6|01|05|1|0||||有|||有||有||有||||J0I0O0W0|JIOO|0|0||J037200021I047200021O024800021O024803029|0|||||1|0#1#0|', 'm0zo2H4IKpP%2Breu60jMsxkl90afv2tG1pwduH8bfcLZlseyjSVc2AZtW6qn2L7xCxuPwCkF3cB79%0A1feEBJegqgp4D3i8VjfhRFUNLCCKkmagdmS3Cc0lpnXUS1XIaXYkhddHW0yJ%2BYTiYxhv5VEEyBbT%0ARNQVH%2FOXyDqf7Q8kfjydMK4HwIA3S%2By8zhw0whwoGSVcTnZz2Cr8gItokMLcrph9N94gK12ORqfw%0AX9tcHTQ8u2w%2BRZreZeIZbveDcbXyakBE3stC5lKtBGnZbnAZlxU67qsQ77VpYVFWmJaJAi7frF5d%0AbpuXJIzmEAhVnTBp|预订|550000D71000|D710|SHH|VNP|SHH|VNP|21:23|09:22|11:59|Y|%2FO3oHcUhuYijOo2I6TN4JmrVWiI3TNq1jgY0sUoM0xIopmwBulpa8YnUhnQ%3D|20210509|3|H6|01|05|1|0||||有|||有||有||有||||J0I0O0W0|JIOO|0|0||J037000021I046900021O024700021O024703029|0|||||1|#1#0|']
    allcheci = data_dict["data"]["result"]
    checimap = data_dict["data"]["map"]
    print("车次\t出发站名\t到达站名\t出发时间\t到达时间\t历时\t一等座\t二等座\t硬卧\t硬座\t无座")
    for i in range(0, len(allcheci)):
        try:
            thischeci = allcheci[i].split("|")
            # 车次---code
            code = thischeci[3]
            # 出发站名---fromname
            fromname = thischeci[6]
            fromname = checimap[fromname]
            # 到达站名---toname
            toname = thischeci[7]
            toname = checimap[toname]
            # 出发时间---stime
            stime = thischeci[8]
            # 到达时间---atime
            atime = thischeci[9]
            # 历时---utime
            utime = thischeci[10]
            # 一等座---ydz
            ydz = thischeci[32]
            # 二等座---edz
            edz = thischeci[31]
            # 硬卧---yw
            yw = thischeci[28]
            # 硬座---yz
            yz = thischeci[29]
            # 无座---wz
            wz = thischeci[26]

            print("\t".join([code,fromname,toname,stime,stime,utime,str(ydz),str(edz),str(yw),str(yz),str(wz)]))
        except Exception as err:
            pass
    isdo = input("查票完成，请输入1继续…")
    if (isdo == 1 or isdo == "1"):
        pass
    else:
        raise Exception("输入不是1，结束执行")

    # 建立 cookie 对象
    print("Cookie处理中…")
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    urllib.request.install_opener(opener)
    #print("cookie: " + str(cjar)) #cookie读取

    # 以下进入自动登录部分
    # loginurl = "https://kyfw.12306.cn/otn/login/init#"
    # req0 = urllib.request.Request(loginurl)
    # req0.add_header('User-Agent',
    #                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
    # req0data = urllib.request.urlopen(req0).read().decode("utf-8", "ignore")
    #
    #

    # ----------------登录时验证码处理--------------------
    while True:
        print("验证码处理开始…")
        callback = "jQuery191013752046252434824_1620460838500"
        callback = "jQuery" + str(random.random()).replace("0.","") + str(random.random()).replace("0.","") + "_" + str(random.random()).replace("0.","")
        use_callback = 0
        # 获取验证码图片
        if use_callback==1:
            yzmurl = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&callback="+callback
        else:
            yzmurl = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand"

        while True:
            yzm_result = urllib.request.urlopen(yzmurl).read().decode("utf-8", "ignore")
            patrst01 = '\"image\":\"(.*?)\"'
            img = re.compile(patrst01).findall(yzm_result)[0]

            img = "data:image/jpg;base64," + img
            urllib.request.urlretrieve(img, filename="yzm.png") # 将图片保存到硬盘中
            yzm = input("请输入验证码，输入第几张图片即可(用逗号分隔,例如：1,2): ")
            if (yzm != "re"):
                break

        allpicpos = "" # 44,47,110,44
        yzm_arr = yzm.split(",")
        for i in yzm_arr:
            thisxy = getxy(int(i))
            for j in thisxy:
                allpicpos = allpicpos + str(j) + ","

        # post验证码验证
        # https://kyfw.12306.cn/passport/captcha/captcha-check?callback=jQuery191013752046252434824_1620460838500&answer=44%2C47%2C110%2C44&rand=sjrand&login_site=E&_=1620460838502
        yzmposturl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        if use_callback==1:
            yzmpostdata = urllib.parse.urlencode({
                "answer": allpicpos,
                "rand": "sjrand",
                "login_site": "E",
                "callback": callback,
            }).encode('utf-8')
        else:
            yzmpostdata = urllib.parse.urlencode({
                "answer": allpicpos,
                "rand": "sjrand",
                "login_site": "E",
            }).encode('utf-8')
        req1 = urllib.request.Request(yzmposturl, yzmpostdata)
        req1.add_header('User-Agent',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
        req1data = urllib.request.urlopen(req1).read().decode("utf-8", "ignore")
        # '/**/jQuery94670896134698561663557843554866_7366223825676806({"result_message":"验证码已经过期","result_code":"7"});'
        # '/**/jQuery35693649539935596098458112133933_9946749976131232({"result_message":"验证码校验成功","result_code":"4"});'
        req1data_result_message = re.compile('\"result_message\":\"(.*?)\"').findall(req1data)[0]
        req1data_result_code = re.compile('\"result_code\":\"(.*?)\"').findall(req1data)[0]
        print(req1data_result_message)
        if (req1data_result_code == 4 or req1data_result_code == '4'):
            break


    # post账号密码验证
    loginposturl = "https://kyfw.12306.cn/passport/web/login"
    loginpostdata = urllib.parse.urlencode({
        "username": USERNAME,
        "password": PASSWORD,
        "appid": "otn",
    }).encode('utf-8')
    login_result = urllib.request.urlopen(urllib.request.Request(loginposturl, loginpostdata, headers=headers))

    # 处理 gzip 压缩的字符串
    encoding = login_result.info().get('Content-Encoding')
    if encoding == 'gzip':
        content2 = gzip.decompress(login_result.read())
    else:
        content2 = login_result.read()
    login_dict = json.loads(content2)




    print("登陆完成")
    isdo = input("如果需要订票，请输入1继续，否则请输入其他数据")
    if (isdo == 1 or isdo == "1"):
        pass
    else:
        raise Exception("输入不是1，结束执行")
    thiscode = input("请输入要预定的车次：")
    chooseno = "None"






    print(img)





import json
import random
if __name__ == '__main__':
    main()


    print("-------------")