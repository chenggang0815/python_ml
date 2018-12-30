import queue
import requests
import datetime
import threading
from lxml import etree
import pandas as pd
import re
import time


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
        # grabs urls of hosts and prints first 1024 bytes of page
            maxTryNum = 10
            for tries in range(maxTryNum):
                try:
                    res=requests.get(url, headers=head).text
                    html=etree.HTML(res)
                    get_url=html.xpath('//a[@class="s xst"]//@href')
                    if len(get_url)==0:
                        continue
                    else:
                        print("解析%d次，成功" % (tries + 1))
                        for i in get_url:
                            url_id.append(str(i)[0:15])
                            url_list.append('http://bbs.51credit.com/' + i)
                        break
                except:
                    if tries < (maxTryNum - 1):
                        print(tries)
                        continue
                    else:
                        print("Has tried %d times to access url %s, all failed!", maxTryNum, url)
                        break
            print(self.getName(),":",url)
            self.queue.task_done()


def main():
    # spawn a pool of threads, and pass them queue instance
    for url in base_url_list:
        q.put(url)
    for i in range(5):
        t = ThreadUrl(q)
        t.setDaemon(True)
        t.start()
    q.join()
            # wait on the queue until everything has been processed


class ThreadUrl2(threading.Thread):
    def __init__(self, queue1,queue2):
        threading.Thread.__init__(self)
        self.queue1 = queue1
        self.queue2 = queue2
    def run(self):
        while True:
            url = self.queue1.get()
            url_id=self.queue2.get()
            res = requests.get(url, headers=head, timeout=100).text
            time.sleep(1)
            html = etree.HTML(res)
            num_page = html.xpath('//div[@class="pg"]//span[@title]//@title')
            if len(num_page) == 0:
                reply_url_list.append('http://bbs.51credit.com/' + url_id + "1" + '-1.html')
            else:
                fin_num_page = int(re.findall('共 (\d*) 页', num_page[0])[0])
                for i in range(1, fin_num_page + 1):
                    reply_url_list.append('http://bbs.51credit.com/' + url_id + str(i) + '-1.html')

            print(self.getName(),":",url)
            self.queue1.task_done()
            self.queue2.task_done()

def main2():
    # spawn a pool of threads, and pass them queue instance
    for url in url_list:
        q1.put(url)
    for id in url_id:
        q2.put(id)
    for i in range(5):
        t = ThreadUrl2(q1,q2)
        t.setDaemon(True)
        t.start()
    q1.join()
    q2.join()


class ThreadUrl3(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            url=self.queue.get()
            for tries in range(5):
                try:
                    res = requests.get(url, headers=head, timeout=100).text
                    time.sleep(1)
                    html = etree.HTML(res)
                    title = html.xpath('//meta[@name="keywords"]//@content')
                    content = html.xpath('//tr/td[@class="t_f"]')
                    author = html.xpath('//div/a[@class="xw1"]')
                    create_time = []
                    tem_create_time = html.xpath('//em[@id]')
                    tem_create_time2 = html.xpath('//em/span[@title]//@title')
                    if len(tem_create_time2) == len(tem_create_time):
                        for i in tem_create_time2:
                            create_time.append(i)
                    else:
                        n = 0
                        for i in tem_create_time:
                            create_time.append(i.text)
                            n = n + 1
                            if n == len(tem_create_time) - len(tem_create_time2):
                                break
                        for i in tem_create_time2:
                            create_time.append(i)

                    delete = html.xpath('//div[@class="locked"]/em')
                    len_detele = len(delete)
                    if tries > 0:
                        print("尝试次数：%d" % (tries + 1))
                    if len(title) == 0 or len(content) == 0 or len(author) == 0 or len(create_time) == 0:
                        continue
                    else:
                        print("解析了%d次,成功" % (tries + 1))
                        break
                except:
                    if tries < (5 - 1):
                        continue
                    else:
                        print("Has tried %d times to access url %s, all failed!", 5, url)
                        break
            if len(title) == 0 or len(content) == 0 or len(author) == 0 or len(create_time) == 0:
                print('这个网页死活解析不出来！！')
            for i in range(len(create_time) - len_detele):
                create_time_list.append(create_time[i])
            for i in content:
                content_list.append(i.text)
                title_list.append(title[0])
                output_url.append(url)
            for i in range(len(author) - len_detele):
                author_list.append(author[i].text)
            print(self.getName(), ":", url)
            self.queue.task_done()


def main3():
    for url in reply_url_list:
        q3.put(url)
    for i in range(5):
        t = ThreadUrl3(q3)
        t.setDaemon(True)
        t.start()
    q3.join()


if __name__ == '__main__':

    starttime = datetime.datetime.now()
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    base_url='http://bbs.51credit.com/forum-216-1.html'
    q=queue.Queue()#存放每个列表页的URL
    q1=queue.Queue()#存放每个帖子的URL
    q2=queue.Queue()#存放每个帖子的ID
    q3=queue.Queue()#存放每页回复的URL
    base_url_list=[]#列表页的URL
    url_id=[]#存放每个帖子的ID
    url_list=[]#列表页中每个帖子的URL
    reply_url_list=[]#每个帖子中，每页回复的URL
    num_page=80 #设置爬取的页数
    create_time_list=[]
    content_list=[]
    title_list=[]
    author_list=[]
    output_url=[]
    for i in range(40,num_page):
        base_url_list.append('http://bbs.51credit.com/forum-216-'+str(i)+'.html')
    print('开始第一个多线程..')
    main()
    print('共得到%d个帖子的URL' % len(url_list))
    print('开始第二个多线程..')
    main2()
    print('共得到%d个回复页的URL' % len(reply_url_list))
    print('开始第三个多线程..')
    main3()
    print(len(content_list))
    print(len(author_list))
    print(len(create_time_list))
    print(len(title_list))
    print(len(output_url))
    data = pd.DataFrame([title_list, content_list, create_time_list, author_list,output_url])
    data = data.T
    data.columns = ['title', 'content', 'time', 'author','URL']
    data.to_excel('我爱卡论坛帖子回复40-80.xlsx')
    endtime=datetime.datetime.now()
    print('共消耗时间：%d秒'%(endtime-starttime).seconds)
