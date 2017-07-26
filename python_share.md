# python爬虫
##目录
* 爬虫原理
* html知识
* requests库与bs4库
* 正则表达式
* 关于反爬虫策略
* 案例分析
* 参考链接及推荐资料
## 爬虫原理
####什么是爬虫？
爬虫是
####WHY PYTHON ?
其实很多语言都可以用来写爬虫，比如java，c#，r元等等，那么为什么大多数都偏爱用python来写爬虫呢？我认为主要有以下原因：
1. 库多！从网页的获取到抓取后的解析，python提供了诸如urllib2，requests，beautifulsoap(简称bs)等这样的工具，可以很方便的帮助我们完成任务。
2. 语法简单！ python的流行很大的原因是由于他的语法简洁，开发速度快，所以才有这样一句话。
> Life is short, I use Python

####爬虫的基本过程
爬虫的基本过程主要分为三大步：**抓取，分析，存储**
1. **其中**，抓取大多数情况属于get请求，即直接从对方服务器上获取数据。一般为html源码或Json格式的字符串。
2. **分析**主要是指从我们抓取到的网页信息中获取我们想要的数据,这一步往往是爬虫过程中最重要的一步。
3. 当然**存储**指的就是如何设置python中的数据结构来存储数据，以及如何将数据写入例如mysql这类的数据库中。
## HTML基础
超文本标记语言（英语：HyperText Markup Language，简称：**HTML**）是一种用于创建网页的标准标记语言。我们对它的掌握只要达到计算机1级的程度就可以了：)
先感受一下：
```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>python爬虫</title>
</head>
<body>
    <h1>我的第一个标题</h1>
    <p>我的第一个段落。</p>
</body>
</html>
```
在上面的这段html代码中，每个tag都代表某个具体的含义：
```
    <!DOCTYPE html> 声明为 HTML5 文档
    <html> 元素是 HTML 页面的根元素
    <head> 元素包含了文档的元（meta）数据
    <title> 元素描述了文档的标题
    <body> 元素包含了可见的页面内容
    <h1> 元素定义一个大标题
    <p> 元素定义一个段落
```
## requests库与bs库
##正则表达式
## 反爬虫策略
###伪装浏览器
有些网站会检查你是不是真的浏览器访问，还是机器自动访问的。这种情况，加上**User-Agent** ，表明你是浏览器访问即可。有时还会检查是否带**Referer**信息还会检查你的Referer是否合法，一般再加上Referer。
```
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
# 伪装成浏览器访问，适用于拒绝爬虫的网站
headers = {'Referer':'XXXXX'}
Requests：
    response = requests.get(url=url, headers=headers)
Urllib2：
    import urllib, urllib2   
    req = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(req)
```
### 时间设置
同样，如果访问频率过快则会被认为异常情况，可能导致爬取失败。Requests，Urllib2都可以使用time库的sleep()函数。
```
import time
time.sleep(1)
```
## 爬取手机贷贴吧数据
**源代码地址:**[程刚-github-爬虫](https://github.com/chenggang0815/python/blob/master/sjd.py)





##推荐资料与参考链接
