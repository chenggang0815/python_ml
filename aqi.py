# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup as bs

head={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:51.0) Gecko/20100101 Firefox/51.0'}

month = ['2015-01','2015-02','2015-03','2015-04','2015-05','2015-06','2015-07','2015-08','2015-09','2015-10','2015-11','2015-12','2016-01','2016-02','2016-03','2016-04','2016-05','2016-06','2016-07','2016-08','2016-09','2016-10','2016-11','2016-12','2017-01']
for i in month:
    url ='https://www.aqistudy.cn/historydata/daydata.php?city=%E4%B8%8A%E6%B5%B7&month='+i
    print(i)
    res = requests.get(url,headers=head)
    soup = bs(res.text)
        #def aqi(soup):#空气质量指数
    saqi = soup.select('tr')
    data = re.findall(r'<td align="center">(.*?)</td>',str(saqi),re.S)
        #186/31=6
    aqi=[]
    for j in range(1,len(data),6):
        aqi.append(data[j])
   # print(aqi)     
    date=[]
    for x in range(0,len(data),6):
        date.append(data[x])
   # print(date)
    with open('aqi.csv','a') as f:
        for y in range(len(date)):
            aqi_data = '%s; %s' % (date[y],aqi[y])
            f.writelines(aqi_data + '\n')
            print('loading...')
            

print('Congratulations!')
            





