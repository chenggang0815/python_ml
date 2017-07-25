print('hello')

# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime

starttime = datetime.datetime.now()


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

base_url = 'https://tieba.baidu.com/f?kw=%E6%89%8B%E6%9C%BA%E8%B4%B7&ie=utf-8'
all_page =165
url_list = []
# 将所有需要爬去的url存入列表
for i in range(0, all_page):
    url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')
    print(i)

res=[];res2=[];res3=[]
for url in url_list:
    res.append(requests.get(url,headers=head))

print(len(res))
for html in res:
    res2.append(html.text.replace('<!--',''))

for html in res2:
    res3.append(html.replace('-->',''))

print(len(res2))
print(len(res3))

soup=[]
for i in res3:
    soup.append(bs(i,'lxml'))

title = [] #标题
author = [] # 作者
time=[] #发帖时间
reply_num=[]#帖子回复数
tiezi_url =[]#帖子ID
first_comment=['目前手机贷客服业务量大增，导致许多用户无法拨通手机贷客服热线']#第一楼
for s in soup:
    a =s.find_all('a',class_='j_th_tit ')
    for i in a:
        title.append(i.string)
        print(i.string)

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
        print(i)
    #第一楼
    f=s.find_all('div', class_='threadlist_abs threadlist_abs_onlyline ')
    for i in f:
        first_comment.append(i.get_text())


print('开始爬取帖子内容')
# 爬取每个帖子里的回复
#===========================================================
all_comment=[] #记录一个帖子内的所有回复
all_user_name=[]
all_comment_time=[]
#all_title=[]
def get_page_num(url):
    res = requests.get(url,headers=head).text
    soup = bs(res,'lxml')
    s=soup.find_all('li',class_='l_reply_num')[2].get_text()
    a=re.findall('共(.*)页',s)
    page_num=int(a[0])
    return  page_num

def get_all_comment(url):
    url_list = []; res = [];soup = [];comment = [];user_name=[];comment_time=[]
    for i in range(1, get_page_num(url)+1):
        url_list.append(url + '?&pn=' + str(i))
        print('页数:')
        print(i)
    for i in url_list:
        res.append(requests.get(i,headers=head).text)
        print(i)
    for i in res:
        soup.append(bs(i,'lxml'))
    for s in soup:
        comment.append(s.find_all('div',class_='d_post_content j_d_post_content '))
        user_name.append(s.find_all('img', username=re.compile('\S')))
        comment_time.append(s.find_all('span', class_='tail-info', text=re.compile('^\d{4}.\d{2}')))  # 只保留时间，用正则表达式匹配开始前四位都是数字的
    for i in comment:
        for j in range(len(i)):
            all_comment.append(i[j].get_text())
    for i in user_name:
        for j in range(len(i)):
            all_user_name.append(i[j].get('username'))
    for i in comment_time:
        for j in range(len(i)):
            all_comment_time.append(i[j].get_text())

for url in tiezi_url:
    print(url)
    get_all_comment(url)


print(len(all_comment))
print(len(all_comment_time))
print(len(all_user_name))

# 导出数据
list_1 = [title,author,time,reply_num,first_comment]
list_2 = [all_comment,all_comment_time,all_user_name]

data1 = pd.DataFrame(list_1)
data2 = pd.DataFrame(list_2)

data1.to_csv('shoujidai_title.csv')
data2.to_csv('shoujidai_comment.csv')

endtime = datetime.datetime.now()

interval = (endtime - starttime).seconds
print(interval)
print('Done!')

'''
soup2=[]
res4=[]
for url in tiezi_url:
    res4.append(requests.get(url, headers=head).text)
    #print('解析帖子url')
    print(url)




for i in res4:
    soup2.append(bs(i,'lxml'))
    #print('添加帖子soup')

title2=[]
comment=[]
item = 0
for s in soup2:
#帖子标题
    title2.append(s.find_all('h3')[0]['title'])
    comment.append(s.find_all('div',class_='d_post_content j_d_post_content '))

for i in comment:
    print(i)

   # for i in range(10):
#     print( s.find_all('div',class_='d_post_content j_d_post_content ')[i].get_text())


'''



