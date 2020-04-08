#-*- coding=utf-8 -*-
#@Time:2020/4/6 10:43
#@Author:大雁
#@File:1.py
#@Software:PyCharm

from  bs4 import BeautifulSoup #网页解析 获取数据
import re  #正则
import urllib.request,urllib.error

import sqlite3  #进行数据库操作
# 影片链接
findLink=re.compile(r'<a href="(.*?)">') #创建正则表达式对象
# 影片图片
findImgSrc=re.compile(r'<img.*?src="(.*?)"',re.S)#re.S 让换行符包含在字符中
# 影片片名
findTitle=re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findCount=re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq=re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)
def mian():
    baseurl="https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist=getData(baseurl)
    
    #数据库保存路径
    dbpath="movie.db"
    savaData2DB(datalist,dbpath)


#1.爬取网页
def getData(baseurl):

    datalist=[]
    for i in range(0,10):
        url=baseurl+str(i*25)
        html=askUrl(url)
        # 2.解析数据
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data=[]
            item=str(item)
            link=re.findall(findLink,item)[0]
            data.append(link)
            IMg=re.findall(findImgSrc,item)[0]
            data.append(IMg)
            Title=re.findall(findTitle,item)
            # print(Title)
            if (len(Title))==2:
                ctitle=Title[0]
                data.append(ctitle) #添加中文名
                otitle=Title[1].replace("/","")#替换空格
                data.append(otitle)#添加国外名
            else:
                data.append(Title[0])
                data.append(" ")#留空
            # 添加评分
            rating=re.findall(findRating, item)[0]
            data.append(rating)

            #  添加评价人数
            count=re.findall(findCount, item)[0]
            data.append(count)
            # 添加概述
            inq=re.findall(findInq, item)

            if len(inq)!=0:
                inq=inq[0].replace("。","")#去掉句号
                data.append(inq)
                # print(inq)
            else:
                data.append(" ")

            bd=re.findall(findBd,item)[0]
            bd=re.sub('<br(\s+)?/>(\s+)?',"  ",bd) #去掉br
            bd=re.sub('/',"",bd)
            data.append(bd.strip()) #去掉前后空格
            datalist.append(data)
    # print(datalist)
    return datalist

# 获取网页内容
def askUrl(url):
    head={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    request=urllib.request.Request(url=url,headers=head)

    html=""
    try:
        respose = urllib.request.urlopen(request)
        html=respose.read().decode("utf-8")


    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


#导入数据库
def savaData2DB(datalist,dbpath):
    ini_db(dbpath)
    conn=sqlite3.connect(dbpath)
    cur=conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index==4 or index==5:
                continue
            data[index]='"'+data[index]+'"'


        sql='''insert into  movie250
                (info_link,pic_link,cname ,ename,score,reted,instroduction,info)
                values (%s)''' %",".join(data)
        
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print("导入完毕！")
#初始换数据库
def ini_db(dbpath):
    sql='''create table movie250
            (
                id  integer primary key autoincrement,
                info_link text,
                pic_link text,
                cname varchar,
                ename varchar,
                score numeric,
                reted numeric,
                instroduction text,
                info text
            );
    '''
    conn=sqlite3.connect(dbpath)
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__=="__main__":
    mian()

