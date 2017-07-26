print('hello')

# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import time

starttime = datetime.datetime.now()


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

base_url = 'https://tieba.baidu.com/f?kw=%E6%89%8B%E6%9C%BA%E8%B4%B7&ie=utf-8'
all_page =160
url_list = []
# 将所有需要爬去的url存入列表
for i in range(0, all_page):
    url_list.append(base_url + '&pn=' + str(50 * i))
    print('第',i+1,'页url已经拼接完成!')


res=[];res2=[];res3=[];i1=0
for url in url_list:
    i1=i1+1
    res.append(requests.get(url,headers=head))
    time.sleep(0.5)
    print('开始对第',i1,'页发起请求')


for html in res:
    res2.append(html.text.replace('<!--',''))

for html in res2:
    res3.append(html.replace('-->',''))

print('替换完所有的注释符号！')

soup=[]
for i in res3:
    soup.append(bs(i,'lxml'))

title = [] #标题
author = [] # 作者
time=[] #发帖时间
reply_num=[]#帖子回复数
tiezi_url =[]#帖子ID
first_comment=['目前手机贷客服业务量大增，导致许多用户无法拨通手机贷客服热线']#第一楼
i3=0
for s in soup:
    i3=i3+1

    a =s.find_all('a',class_='j_th_tit ')
    for i in a:
        title.append(i.string)

    b = s.find_all('span', title=re.compile('(主题作者.*)'))
    for i in b:
        author.append(i.get_text())

    c = s.find_all('span',class_='pull-right is_show_create_time')
    for i in c:
        time.append(i.get_text())

    d= s.find_all('span',class_='threadlist_rep_num center_text')
    for i in d:
        reply_num.append(i.get_text())

    e = s.find_all('a', class_='j_th_tit ')

    for i in e:
        tiezi_url.append('https://tieba.baidu.com'+i.get('href'))
    #第一楼
    f=s.find_all('div', class_='threadlist_abs threadlist_abs_onlyline ')
    for i in f:
        first_comment.append(i.get_text())
    print('第', i3, '页帖子数据爬取完毕')

# 导出数据
print('导出帖子标题数据！')
list_1 = [title,author,time,reply_num,first_comment]
data1 = pd.DataFrame(list_1)
data1.T.to_csv('shoujidai_title.csv')

print('开始爬取每个帖子的回复内容...')
print('正在爬取第一个帖子的回复内容...')
# 爬取每个帖子里的回复
#===========================================================
all_comment=[] #记录一个帖子内的所有回复
all_user_name=[]
all_comment_time=[]
all_title=[]
def get_page_num(url):
    res = requests.get(url,headers=head).text
    soup = bs(res,'lxml')
    if soup.find('title').get_text()=='贴吧404':
        page_num = 0
        return page_num
    else:
        try:
            s = soup.find_all('li', class_='l_reply_num')[2].get_text()
        except:
            page_num = 0
            return page_num
        else:
            a = re.findall('共(.*)页', s)
            page_num = int(a[0])
            return page_num



def get_all_comment(url):
    url_list = []; res = [];soup = [];comment = [];user_name=[];comment_time=[]
    for i in range(1, get_page_num(url)+1):
        if get_page_num(url) ==0:
            continue
        url_list.append(url + '?&pn=' + str(i))
    for i in url_list:
        res.append(requests.get(i,headers=head).text)
    for i in res:
        soup.append(bs(i,'lxml'))
    for s in soup:
        comment.append(s.find_all('div',class_='d_post_content j_d_post_content '))
        user_name.append(s.find_all('img', username=re.compile('\S')))
        comment_time.append(s.find_all('span', class_='tail-info', text=re.compile('^\d{4}.\d{2}')))  # 只保留时间，用正则表达式匹配开始前四位都是数字的
    for i in comment:
        for j in range(len(i)):
            all_comment.append(i[j].get_text())
            all_title.append(title[i5-1])
    for i in user_name:
        for j in range(len(i)):
            all_user_name.append(i[j].get('username'))
    for i in comment_time:
        for j in range(len(i)):
            all_comment_time.append(i[j].get_text())

i5=0
for url in tiezi_url:
    i5=1+i5
    get_all_comment(url)
    print('共有',all_page*50,'个帖子','已经爬取了第',i5,'个帖子')

print(len(all_comment))
print(len(all_comment_time))
print(len(all_user_name))

# 导出数据
list_2 = [all_title,all_comment,all_comment_time,all_user_name]

data2 = pd.DataFrame(list_2)



print('开始导出回复数据！')
data2.T.to_csv('shoujidai_comment.csv')

endtime = datetime.datetime.now()
interval = (endtime - starttime).seconds
print('共消耗时间：',interval,'秒')
print('Done!')

