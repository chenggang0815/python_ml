# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import time
import threading
import queue
from lxml import etree
import random

start_time=datetime.datetime.now()
#head={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.0.3; HTC T328d Build/IML74K)'}
cookie={"Cookie":"_T_WM=d673d69859a47cabaa24ab80a05992b4; SCF=AvuMg7xpZ3MixxIfg_RBa-WAjMnLdtNLLXPz6xs2WQqOCHq3ZYxgLZqK8SWAF3H3nWQzRF1-Qesbgp56eE_qh_M.; SUB=_2A250qnewDeRhGeNO6loW-S_FzT-IHXVUVRn4rDV6PUJbkdBeLRbtkW1lSJcpCI1hAOmMmDL_HDUgbZT2Hw..; SUHB=0jBI8QbUuFy2lm; SSOLoginState=1504577504"}
# s=requests.Session()
# login_data={'username':'13052003867','password':'*Cheng1995'}
# s.post('https://passport.weibo.cn/signin/login',login_data)
#res=requests.get('https://weibo.cn/5018791963?since_id=FjvkBzJCu&max_id=Fjpfnojn8&prev_page=2&page=1',cookies = cookie).text
base_url='https://weibo.cn/ppdai07?page='
res=[]
num_page=180
url_list=[]
for i in range(80,num_page):
    url_list.append(base_url+str(i))
for url in url_list:
    print(url)
    res.append(requests.get(url,cookies=cookie).text)
    print(res)
    s=random.randint(0,2)
    time.sleep(s)



final_content=[]
final_author=[]
final_time=[]
comment_url=[]
for i in res:
    soup=bs(i,'lxml')
    href = soup.find_all('a')
    comment=soup.find_all('a',class_='cc') #提取评论的URL
    for i in comment:
        if i.get_text() != '评论[0]':
            comment_url.append(i['href'])


print('开始去除手机贷转发的微博..只看第一次原创的微博')
for i in comment_url:
    if '1894964897' not in i:
        comment_url.remove(i)

print('开始计算每条微博的评论有多少页..')
time.sleep(2)
print(len(comment_url))
page_num=[]
n1=0
for i in comment_url:
    for item in  range(20):
        res=requests.get(i,cookies=cookie).text
        print(i)
        print('=====================')
        print(res)
        if len(res)==0:
            print('已循环：',item)
            continue
        else:
            t=random.randint(0,2)
            time.sleep(t)
            s=str(res)
            page=re.findall('value="跳页" />&nbsp;1/(.*?)页',s)
            if len(page)==0:
                page_num.append(0)
            else:
                page_num.append(int(page[0]))
            n1=n1+1
            print('共有%d条微博评论需要计算页数,已计算%d条'%(len(comment_url),n1))
            break


'''auhotr = soup.find_all('a',class_='nk')
for i in auhotr:
    print(i.get_text())
    final_author.append(i.get_text())
'''

print('计算完评论的页数,开始拼接所有的评论URL...')
n=0
all_comment_url=[]
for url in comment_url:
    url=url[:-7]
    for i in range(0,page_num[n]+1):
        all_comment_url.append(url+'&page='+str(i))
    n=n+1
    # for j in
print('拼接完毕,开始抓取所有评论过的用户...')
all_comment_user_id=[];all_phone=[];all_content=[]
n2=0
for url in all_comment_url:
        res=requests.get(url,cookies=cookie).text
        t = random.randint(0, 2)
        time.sleep(t)
        print(url)
        print('=============================')
        print(res)
        s=str(res)
        # phone=re.findall('来自(.*?)    </span>',s)
        # for i in phone:
        #     all_phone.append(i)
        soup=bs(res,'lxml')
        # content=soup.find_all('span',class_='ctt')
        # content=content[1:]
        # for i in content:
        #     all_content.append(i.get_text())
        uid=soup.find_all('a')
        for i in uid:
            id=re.findall('&amp;fuid=(.*)&amp;type=2',str(i))
            for j in id:
                all_comment_user_id.append(j)
        n2 = n2 + 1
        print('共有%d条评论页需要抓取用户,已抓取%d条' % (len(all_comment_url), n2))

# print(len(all_content))
# print(len(all_phone))


all_comment_user_id=list(set(all_comment_user_id))
all_comment_user_url=[];all_comment_userinfo_url=[]
for id in all_comment_user_id:
    all_comment_user_url.append('https://weibo.cn/u/'+str(id))
    all_comment_userinfo_url.append('https://weibo.cn/'+str(id)+'/info')


print(len(all_comment_userinfo_url))
user_data=pd.DataFrame([all_comment_userinfo_url]).T
user_data.to_excel('用户主页80-180.xlsx')


# content = pd.DataFrame([all_comment_user_id,all_content,all_phone]).T
# content.to_excel('内容及手机型号.xlsx')
print('导出成功！')
end_time=datetime.datetime.now()
print('总消耗时间：%d秒'%(end_time-start_time).seconds)
