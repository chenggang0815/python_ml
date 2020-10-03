# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup
import datetime
import time

'''
爬取全国哲学社会科学工作办公室文章
'''


def get_all_url(base_url, page_num, head):
    res = []
    for i in range(1, page_num):
        url = base_url + 'index' + str(i) + '.html'
        content = requests.get(url, headers=head).content
        bs = BeautifulSoup(content, 'lxml')
        res.append(bs)
        time.sleep(0.5)

    url_article = []  # 文章url
    for s in res:
        a = s.find_all('a', href=re.compile('(/n1.*)'))
        for item in a:
            url_article.append('http://www.nopss.gov.cn' + item.get('href'))

    return url_article


def get_all_article(url_list, head):
    res = []
    i = 0
    for url in url_list:
        i = i + 1
        content = requests.get(url, headers=head).content
        bs = BeautifulSoup(content, 'lxml')
        res.append(bs)
        time.sleep(0.5)
        print('一共 %s 篇文章，开始对第 %s 篇文章发起请求' % (len(url_list), i))

    for s in res:
        title_list = s.find_all('h1')
        for item in title_list:
            with open("D:\\code\\python_ml\\python_crawler\\philosophy.txt", "a", encoding='utf-8') as f:
                f.write('========================================================' + '\n')
                f.write(item.get_text() + '\n')

        content_list = s.find_all('p')
        for item in content_list:
            with open("D:\\code\\python_ml\\python_crawler\\philosophy.txt", "a", encoding='utf-8') as f:
                f.write(item.get_text() + '\n')


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    base_url = 'http://www.nopss.gov.cn/GB/373410/'
    num_page = 6

    all_article_url = get_all_url(base_url, num_page, head)
    get_all_article(all_article_url, head)

    end_time = datetime.datetime.now()
    interval = (end_time - start_time).seconds
    print('共消耗时间：', interval, '秒')
