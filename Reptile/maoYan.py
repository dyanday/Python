#-*- coding=utf-8 -*-
#@Time:2020/4/9 9:42
#@Author:大雁
#@File:maoYan.py
#@Software:PyCharm
import requests
import re
import json

from multiprocessing  import Pool

#爬取源代码
def get_one_page(url):

    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    respose=requests.get(url=url,headers=headers)
    html=respose.content.decode("utf-8")
    return html


#解析源码
def get_one_screen(html):
    index = re.compile('<dd>.*?board-index.*?(\d+)</i>.*?data-src="(.*?)" alt="(.*?)" class.*?star">(.*?)</p>'
                       '.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(\d+)</i>',re.S)
    items=re.findall(index,html)
    for  item in items:
        yield {
            'id':item[0],
            '图片':item[1],
            '电影':item[2],
            '主演':item[3].strip()[3:],
            '上映时间':item[4].strip()[5:],
            "评分":item[5]+item[6]
        }

def write_to_file(content):
    with open("猫眼电影top100.json","a",encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+','+'\n')
        f.close()

def main(offset):
    url = "https://maoyan.com/board/4?offset="+str(offset)
    html=get_one_page(url)

    for item in get_one_screen(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    pool=Pool()
    pool.map(main,[i*10 for i in range(10)])
    print("导入完毕！")




