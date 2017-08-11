print('hello')

# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import time
from lxml import etree


starttime = datetime.datetime.now()
base_url='http://bbs.51credit.com/forum-216-1.html'

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

url_list = [];url_id=[]
def Get_list_url(base_url, maxTryMum):
    for tries in range(1,maxTryMum):
        res=requests.get(base_url,headers=head,timeout=100).text
        time.sleep(0.2)
        html=etree.HTML(res)
        get_url=html.xpath('//a[@class="s xst"]//@href')
        if len(get_url)==0:
            continue
        else:
            print("解析%d次，成功" % tries)
            for i in get_url:
                url_id.append(str(i)[0:15])
                url_list.append('http://bbs.51credit.com/'+i)
            break
    return url_list



reply_url_list=[]
def Get_reply_url(url,url_id):
    res = requests.get(url, headers=head, timeout=100).text
    time.sleep(0.2)
    html = etree.HTML(res)
    num_page = html.xpath('//div[@class="pg"]//span[@title]//@title')
    if len(num_page) == 0:
        reply_url_list.append('http://bbs.51credit.com/'+ url_id + "1" + '-1.html')
    else:
        fin_num_page = int(re.findall('共 (\d*) 页', num_page[0])[0])
        for i in range(1,fin_num_page+1):
            reply_url_list.append('http://bbs.51credit.com/'+ url_id + str(i) + '-1.html')
                #print('http://bbs.51credit.com/'+ url_id + str(i) + '-1.html')
    return  reply_url_list




title_list=[]
content_list=[]
author_list=[]
create_time_list =[]


def Open_Link(url,maxTryNum):
    title=[];content=[];author=[];create_time=[];delete=[];len_detele=0
    print('正在解析url：%s' % url)
    for tries in range(maxTryNum):
        try:
            res =requests.get(url, headers=head,timeout=100).text
            time.sleep(0.2)
            html = etree.HTML(res)
            title = html.xpath('//meta[@name="keywords"]//@content')
            content = html.xpath('//tr/td[@class="t_f"]')
            author = html.xpath('//div/a[@class="xw1"]')
            create_time= html.xpath('//em/span[@title]//@title')
            delete = html.xpath('//div[@class="locked"]/em')
            len_detele=len(delete)
            print('共有多少条回复被删除:%d' % len_detele)
            if len(title) == 0 or len(content) == 0 or len(author) == 0 or len(create_time) == 0:
                continue
            else:
                print("解析了%d次,成功" % tries)
                break
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                print("Has tried %d times to access url %s, all failed!", maxTryNum, url)
                break

    if len(title) == 0 or len(content) == 0 or len(author) == 0 or len(create_time) == 0:
        print('这个网页死活解析不出来！！')

    for i in range(len(create_time)-len_detele):
        create_time_list.append(create_time[i])
    for i in content:
        content_list.append(i.text)
        title_list.append(title[0])
    for i in range(len(author)-len_detele):
        author_list.append(author[i].text)


Get_list_url(base_url,15)
print("开始解析回复页！")
for i in range(len(url_list)):
    Get_reply_url(url_list[i], url_id[i])
    print(i)


print("解析完成")
print(len(reply_url_list))

n=1
for i in reply_url_list:
    print(i)
    print("共有%d条url，已经解析%d条" %(len(reply_url_list),n))
    Open_Link(i,15)
    n = n +1






data=pd.DataFrame([title_list,content_list,create_time_list,author_list])
data=data.T
data.columns=['title','content','time','author']
data.to_excel('我爱卡论坛帖子回复.xlsx')

print(len(content_list))
print(len(author_list))
print(len(create_time_list))
print(len(title_list))

endtime = datetime.datetime.now()
interval = (endtime - starttime).seconds
print('共消耗时间：',interval,'秒')
print('Done!')







'''
for i in range(100):
    res = requests.get(base_url, headers=head).text
    html = etree.HTML(res)
    title = html.xpath('//a[@class="s xst"]')
    author = html.xpath('//a[@href= ]')
    print("已经尝试了%d次" % i)
    time.sleep(1)
    if len(title) == 0:
        continue
    else:
        print('result非空')
        break


for i in title:
    print(i.text)

for i in author:
    print(i.text)

print(len(title))
print(len(author))

'''
