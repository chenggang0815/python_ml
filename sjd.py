# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup as bs
import re

head = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:51.0) Gecko/20100101 Firefox/51.0'}

url = 'https://tieba.baidu.com/f?ie=utf-8&kw=%E6%89%8B%E6%9C%BA%E8%B4%B7&fr=search'

res = requests.get(url,headers=head)

res2 = res.text.replace('<!--','')
res3 = res2.replace('-->','')

soup = bs(res3,'lxml')
#print(soup.body.a)

#url = 'https://tieba.baidu.com/f?kw=%E6%89%8B%E6%9C%BA%E8%B4%B7&ie=utf-8&pn=50'


#for i in page:
 #   url ='https://www.aqistudy.cn/historydata/daydata.php?city=%E4%B8%8A%E6%B5%B7&month='+i
  #  print(i)
   # res = requests.get(url,headers=head)

#soup = bs(res.text)

title = []

print('title-----------------------------------')
a =soup.find_all('a',class_='j_th_tit ')
print(type(a))
for i in a:
   # print(i.string)
    title.append(i.string)

author = []
print('author-------------------------------')
b = soup.find_all('span', class_='tb_icon_author ')
print(type(b))
for i in b:
    #print(i.get_text())
    author.append(i.get_text())

time=[]
print('time---------------------------------')
c = soup.find_all('span',class_='pull-right is_show_create_time')
for i in c:
    #print(i.get_text())
    time.append(i.get_text())

reply_num=[]
print('reply_num---------------------------------')
d= soup.find_all('span',class_='threadlist_rep_num center_text')
for i in d:
    #print(i.get_text())
    reply_num.append(i.get_text())

print(len(title))
print(len(time))
print(len(author))
print(len(reply_num))
'''with open('shoujidai.csv','a') as f:
    for y in range(50):
        sjd_data = '%s; %s; %s; %s' % (title[y],author[y],time[y],reply_num[y])
        f.writelines(sjd_data + '\n')
print('loading...')'''


#print(type(res.text))

#print(soup.title)
#print(soup.p)
#print(soup.a)

#print(soup.body)

