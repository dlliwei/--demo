import urllib.request
import http.cookiejar
import pymysql

conn = pymysql.connect(host="127.0.0.1",user="root", passwd="123456", db="news")
def main():
    name1 = "zhangsan"
    pass1 = "aaa"
    name2 = "lisi"
    pass2 ="bbb"

    # insert into user(name,password) values('name1','pass1'),('name2','pass2')
    conn.query("insert into user(name,password) values('"+ str(name1) +"','"+ str(pass1) +"'),('"+ str(name2) +"','"+ str(pass2) +"')")
    conn.commit()



if __name__ == '__main__':
    main()