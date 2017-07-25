print('hello')

# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup as bs

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

'''
url = 'https://tieba.baidu.com/f?kw=%E6%89%8B%E6%9C%BA%E8%B4%B7&ie=utf-8&pn=50'

res = requests.get(url,headers=head)

res2 = res.text.replace('<!--','')
res3 = res2.replace('-->','')

soup = bs(res3,'lxml')'''
#print(soup.body.a)

base_url = 'https://tieba.baidu.com/f?kw=%E6%89%8B%E6%9C%BA%E8%B4%B7&ie=utf-8'
deep =1
url_list = []
# 将所有需要爬去的url存入列表
for i in range(0, deep):
    url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')

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
for s in soup:
    print('title-----------------------------------')
    a =s.find_all('a',class_='j_th_tit ')
    for i in a:
        title.append(i.string)



    print('author-------------------------------')
    b = s.find_all('span', title=re.compile('(主题作者.*)'))
    for i in b:
        author.append(i.get_text())


    print('time---------------------------------')
    c = s.find_all('span',class_='pull-right is_show_create_time')
    for i in c:
        time.append(i.get_text())

    print('reply_num---------------------------------')
    d= s.find_all('span',class_='threadlist_rep_num center_text')
    for i in d:
        reply_num.append(i.get_text())

    print('title_id----------------------------------')
    e = s.find_all('a', class_='j_th_tit ')
    for i in e:
        tiezi_url.append('https://tieba.baidu.com'+i.get('href'))

#    for  i in tiezi_url:
#        print(i)

print('开始爬取帖子内容')
# 爬取每个帖子里的回复

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
for s in soup2:
#帖子标题
    title2.append(s.find_all('h3'))
    print(s.find_all('h3')[0]['title'])
    print(type(s.find_all('h3')))
    #print(s.html)

for i in title2:
    print(re.findall('">(.*)</h3>',i))

print('Done!')



#print(len(title))
#print(len(time))
#print(len(author))
#print(len(reply_num))
#print(len(tiezi_url))
'''
with open('shoujidai.csv','a') as f:
    for y in range(150):
        sjd_data = '%s; %s; %s; %s' % (title[y],author[y],time[y],reply_num[y])
        f.writelines(sjd_data + '\n')
        print('loading...')'''





