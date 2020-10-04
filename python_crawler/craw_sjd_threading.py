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


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            res = requests.get(url, headers=head).text
            res = res.replace('<!--', '')
            res = res.replace('-->', '')
            soup = bs(res,'lxml')
            a = soup.find_all('a', class_='j_th_tit ')
            for i in a:
                title.append(i.string)
            id = soup.find_all('a', class_='j_th_tit ')
            for i in id:
                tiezi_url.append('https://tieba.baidu.com' + i.get('href'))

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


class ThreadUrl2(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            get_all_comment(url)

            print(self.getName(),":",url)
            self.queue.task_done()


def main2():
    # spawn a pool of threads, and pass them queue instance
    for url in tiezi_url:
        q2.put(url)
    for i in range(20):
        t = ThreadUrl2(q2)
        t.setDaemon(True)
        t.start()
    q2.join()


def open_link(url):
    try_num = 10
    for tries in range(try_num):
        try:
            res =requests.get(url, headers=head, timeout=100).text
            time.sleep(0.2)
            break
        except:
            if tries < (try_num - 1):
                continue
            else:
                print("Has tried %d times to access url %s, all failed!", try_num, url)
                break
    return res


def get_page_num(url):
    res = open_link(url)
    soup = bs(res, 'lxml')
    if soup.find('title').get_text() == '贴吧404' or soup.find('title').get_text() == '404 Not Found':
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
    url_list = []; res = [];soup = [];comment = [];user_name=[];comment_time=[];html=[];title=[]
    for i in range(1, get_page_num(url)+1):
        if get_page_num(url) ==0:
            continue
        url_list.append(url + '?&pn=' + str(i))
    for i in url_list:
        res.append(open_link(i))
    for i in res:
        soup.append(bs(i,'lxml'))
        html.append(etree.HTML(i))
    for h in html:
        comment_time=h.xpath('//div/span[@class="tail-info"]')
        for i in comment_time:
            if re.findall('(.*)\d-\d{2}-\d{2}', i.text) == ['201']:
                all_comment_time.append(i.text)
    for s in soup:
        comment.append(s.find_all('div',class_='d_post_content j_d_post_content '))
        user_name.append(s.find_all('img', username=re.compile('\S')))
    n = 0
    for i in comment:
        n = n+1
        for j in range(len(i)):
            all_comment.append(i[j].get_text())
            #all_title.append(title[n-1])

    for i in user_name:
        for j in range(len(i)):
            all_user_name.append(i[j].get('username'))


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    base_url = 'https://tieba.baidu.com/f?kw=手机贷&ie=utf-8'
    q = queue.Queue()  # 存放每个列表页的URL
    q2 = queue.Queue()  # 存放每个列表页的URL
    all_comment = []  # 记录一个帖子内的所有回复
    all_user_name = []
    all_comment_time = []
    all_title = []
    title = []

    base_url_list = []
    tiezi_url = []
    num_page = 120
    for i in range(0, num_page):
        base_url_list.append(base_url+ '&pn=' + str(50 * i))
        print('https://tieba.baidu.com/f?kw=%E9%80%BE%E6%9C%9F&ie=utf-8'
              + '&pn=' + str(50 * i))
    print('开始第一个多线程..')
    main()
    print('开始第二个多线程..')
    main2()
    print(len(all_comment))
    print(len(all_comment_time))
    print(len(all_user_name))
    # 导出数据
    list_2 = [all_comment, all_comment_time, all_user_name]
    data2 = pd.DataFrame(list_2)
    data2 = data2.T
    data2.columns = ['reply_content', 'reply_time', 'author']
    print('开始导出回复数据！')
    data2.to_csv('手机贷吧帖子回复.csv')
    end_time = datetime.datetime.now()
    print('共消耗时间：%d秒' % (end_time - start_time).seconds)
