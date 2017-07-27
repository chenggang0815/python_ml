# Python爬虫实战（一次走心的分享）

## 数据决策部   

### 程刚

### 目录

* 爬虫原理
* html知识
* 正则表达式
* requests库与bs4库
* 关于反爬虫策略
* 案例分析
* 参考链接及推荐资料
## 爬虫原理
#### 什么是爬虫？
网络爬虫是一个自动提取网页的程序，它从万维网上下载网页，是搜索引擎的重要组成。传统爬虫从一个或若干初始网页的URL开始，获得初始网页上的URL，在抓取网页的过程中，不断从当前页面上抽取新的URL放入队列,直到满足系统的一定停止条件。

#### WHY PYTHON ?
其实很多语言都可以用来写爬虫，比如java，c#，r元等等，那么为什么大多数都偏爱用python来写爬虫呢？我认为主要有以下原因：
1. 库多！从网页的获取到抓取后的解析，python提供了诸如urllib2，requests，beautifulsoap(简称bs)等这样的工具，可以很方便的帮助我们完成任务。
2. 语法简单！ python的流行很大的原因是由于他的语法简洁，开发速度快，所以才有这样一句话。
> Life is short, I use Python

#### 爬虫的基本过程
爬虫的基本过程主要分为三大步：**抓取，分析，存储**
1. **其中**，抓取大多数情况属于get请求，即直接从对方服务器上获取数据。一般为html源码或Json格式的字符串。
2. **分析**主要是指从我们抓取到的网页信息中获取我们想要的数据,这一步往往是爬虫过程中最重要的一步。
3. 当然**存储**指的就是如何设置python中的数据结构来存储数据，以及如何将数据写入例如mysql这类的数据库中。
## HTML基础
**什么是html?**

* HTML 不是一种编程语言，而是一种**标记**语言
* 标记语言是一套**标记标签** (markup tag)
* HTML 使用标记标签来**描述**网页
* HTML 文档包含了HTML** 标签**及**文本**内容

**超文本标记语言**（英语：HyperText Markup Language，简称：**HTML**）是一种用于创建网页的标准标记语言。我们对它的掌握只要达到计算机1级的程度就可以了：)
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
**什么是html标签？**

HTML 标记标签通常被称为 HTML 标签 (HTML tag)。

- HTML 标签是由*尖括号*包围的关键词，比如 <html>
- HTML 标签通常是*成对出现*的，比如 <b> 和 </b>
- 标签对中的第一个标签是**开始标签**，第二个标签是**结束标签**

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
Web浏览器（如谷歌浏览器，Internet Explorer，Firefox，Safari）是用于读取HTML文件，并将其作为网页显示。浏览器并不是直接显示的HTML标签，但可以使用标签来决定如何展现HTML页面的内容给用户。

**而爬虫说到底就是要模拟浏览器的行为，我们同样需要读取HTML文件，只不过不用将它作为网页显示，而是从中读取想要的数据。**

关于html更多的知识，请参考[菜鸟学院](https://www.runoob.com/html/html-tutorial.html)

## 正则表达式

**什么是正则表达式？**

**正则表达式**，又称规则表达式**。**（英语：Regular Expression，在代码中常简写为regex、regexp或RE），计算机科学的一个概念。**正则表通常被用来检索、替换那些符合某个模式(规则)的文本。**

**re** 模块使 Python 语言拥有全部的正则表达式功能。

**正则表达式中常用的字符含义 ：**

| 普通字符 | 匹配自身                                     | abc                  | abc         |
| ---- | ---------------------------------------- | -------------------- | ----------- |
| .    | 匹配任意除换行符"\n"外的字符(在DOTALL模式中也能匹配换行符       | a.c                  | abc         |
| \    | 转义字符，使后一个字符改变原来的意思                       | a\.c;a\\c            | a.c;a\c     |
| *    | 匹配前一个字符0或多次                              | abc*                 | ab;abccc    |
| +    | 匹配前一个字符1次或无限次                            | abc+                 | abc;abccc   |
| ?    | 匹配一个字符0次或1次                              | abc?                 | ab;abc      |
| ^    | 匹配字符串开头。在多行模式中匹配每一行的开头                   | ^abc                 | abc         |
| $    | 匹配字符串末尾，在多行模式中匹配每一行的末尾                   | abc$                 | abc         |
| \|   | 或。匹配\|左右表达式任意一个，从左到右匹配，如果\|没有包括在()中，则它的范围是整个正则表达式 | abc\|def             | abcdef      |
| {}   | {m}匹配前一个字符m次，{m,n}匹配前一个字符m至n次，若省略n，则匹配m至无限次 | ab{1,2}c             | abcabbc     |
| []   | 字符集。对应的位置可以是字符集中任意字符。字符集中的字符可以逐个列出，也可以给出范围，如[abc]或[a-c]。[^abc]表示取反，即非abc。所有特殊字符在字符集中都失去其原有的特殊含义。用\反斜杠转义恢复特殊字符的特殊含义。 | a[bcd]e              | abeaceade   |
| ()   | 被括起来的表达式将作为分组，从表达式左边开始没遇到一个分组的左括号“（”，编号+1.分组表达式作为一个整体，可以后接数量词。表达式中的\|仅在该组中有效。 | (abc){2}a(123\|456)c | abcabca456c |

这里需要强调一下反斜杠\的作用：

* 反斜杠后边跟元字符去除特殊功能；（即将特殊字符转义成普通字符）
* 反斜杠后边跟普通字符实现特殊功能；（即预定义字符）

**预定义字符集（可以写在字符集[...]中） **

| \d   | 数字:[0-9]                                 | a\bc          | a1c         |
| ---- | ---------------------------------------- | ------------- | ----------- |
| \D   | 非数字:[^\d]                                | a\Dc          | abc         |
| \s   | 匹配任何空白字符:[<空格>\t\r\n\f\v]                | a\sc          | a c         |
| \S   | 非空白字符:[^\s]                              | a\Sc          | abc         |
| \w   | 匹配包括下划线在内的任何字字符:[A-Za-z0-9_]             | a\wc          | abc         |
| \W   | 匹配非字母字符，即匹配特殊字符                          | a\Wc          | a c         |
| \A   | 仅匹配字符串开头,同^                              | \Aabc         | abc         |
| \Z   | 仅匹配字符串结尾，同$                              | abc\Z         | abc         |
| \b   | 匹配\w和\W之间，即匹配单词边界匹配一个单词边界，也就是指单词和空格间的位置。例如， 'er\b' 可以匹配"never" 中的 'er'，但不能匹配 "verb" 中的 'er'。 | \babc\ba\b!bc | 空格abc空格a!bc |
| \B   | [^\b]                                    | a\Bbc         | abc         |

还是来看个简单的例子：

```
import re
a='ddsdfksfsdklovegfdg'
print(re.findall('dk(.*)gf'),a)
#'love'
```

我们可以感受到正则表达式的灵活与强大，但是我们不必死记硬背，只需要记住最常用的几个组合就足够了！

* 关于正则表达式的学习资料请看这里：[Python正则表达式](https://www.runoob.com/python/python-reg-expressions.html)

## requests库与bs库

使用**requests**发送网络请求非常容易，其中最常用的是get请求。

```
import requests
r = requests.get(url='http://www.itwhy.org')    # 最基本的GET请求，返回一个response对象
print(r.status_code)    # 获取返回状态
print(r.url)
print(r.text)   #打印解码后的返回数据
```

**beautifulsoup**可以帮助我们可以很方便地提取出HTML或XML标签中的内容,下来来举个栗子：

```
html="<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>python爬虫</title>
</head>
<body>
    <h1>我的第一个标题</h1>
    <p>我的第一个段落。</p>
    <p>我的第二个段落。</p>
    <a>共1页。</a>
</body>
</html>"
```

假设这是我们发起网络请求返回的html文件，现在我们来建立一个beautifulsoup 对象：

```
from bs4 import BeautifulSoup as bs
soup = bs(html)
```

如果我们要返回title标签里的内容，只需要一行代码：

```
print(soup.title.string)
#python爬虫
```

其中，`find()`方法会返回符合条件的第一个节点，`find_all()` 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件，也只需要一行代码：

```
print(soup.find_all('p'))
 #<p>我的第一个段落。</p>
 #<p>我的第二个段落。</p>
 a=print(soup.find_all('p'))
 for i in a:
      print(i.string)
 #我的第一个段落。
 #我的第二个段落。
```

`find_all`函数最强大的是它还可以和正则表达式结合起来，比如要提取“共1页”中的页数，

```
print(soup.find('a',text=re.compile('共(.*)页')))
#1
```

* 有关requests的更多介绍请参考这里：[**python request第三方库介绍**](http://blog.csdn.net/chdhust/article/details/50537137)
* 有关beautifulsoup的更多介绍请看这里：[Python爬虫入门（8）：Beautiful Soup的用法](http://python.jobbole.com/81349/)



## 反爬虫策略

#### 采用代理ip

当自己的ip被网站封了之后，可以采取换代理ip的方式进行爬取。当一个代理ip挂了之后怎么办？**可以做个ip池，把一堆代理ip放在一起，每次运行时从ip池挑一个代理ip当做访问ip就可以了！**

参考链接：[建立爬虫代理IP池](https://zhuanlan.zhihu.com/p/25285987)

#### 伪装浏览器

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
#### 时间设置

同样，如果访问频率过快则会被认为异常情况，可能导致爬取失败。我们可以每抓取一个页面就休息随机秒。Requests，Urllib2都可以使用time库的sleep()函数。

```
import time
time.sleep(1)
```
关于反爬虫的学习资料，可以看这里：

* [当爬虫不遵守 robots 协议时，有没有防止抓取的可能?](https://www.zhihu.com/question/22324380/answer/120093636)
* [关于反爬虫，看这一篇就够了](http://geek.csdn.net/news/detail/85333)

**总结：**

> **在爬虫与反爬虫的对弈中，爬虫一定会胜利。**换言之，只要人类能够正常访问的网页，爬虫在具备同等资源的情况下就一定可以抓取到。

#### 使用cookie登陆

> Cookie，有时也用其复数形式 [Cookies](https://baike.baidu.com/item/Cookies/187064)，指某些网站为了辨别用户身份、进行 session 跟踪而储存在用户本地终端上的数据（通常经过加密）

使用cookie登陆，服务器会认为你是一个已登陆的用户，所以就会返回给你一个已登陆的内容。因此，需要验证码的情况可以使用带验证码登陆的cookie解决。

参考资料：[python3爬虫 - cookie登录实战 ](http://blog.csdn.net/pipisorry/article/details/47948065)

#### 动态页面

> 当我们进行网页爬虫时，我们会利用一定的规则从返回的 HTML 数据中提取出有效的信息。但是如果网页中含有 JavaScript 代码，我们必须经过渲染处理才能获得原始数据。此时，如果我们仍采用常规方法从中抓取数据，那么我们将一无所获。

遇到动态页面可以使用python中的selenium库。

> 官方文档[Selenium with Python](https://link.zhihu.com/?target=http%3A//selenium-python.readthedocs.io/index.html)，简单来说就是模拟人对浏览器的动作，可以用代码打开你的浏览器然后像人一样操作实现浏览器的自动化（打开网页、输入文字、提交表单等），安装等详细介绍在官方文档中有介绍。

关于动态页面的爬取可以参考：

* [请问爬虫如何爬取动态页面的内容？](https://www.zhihu.com/question/46528604?sort=created)
* [爬虫技术:(JavaScript渲染)动态页面抓取超级指南](http://python.jobbole.com/84600/)

#### Scrapy

> Scrapy，Python开发的一个快速,高层次的屏幕抓取和web抓取框架，用于抓取web站点并从页面中提取结构化的数据。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试。
>
> Scrapy吸引人的地方在于它是一个框架，任何人都可以根据需求方便的修改。它也提供了多种类型爬虫的基类，如BaseSpider、sitemap爬虫等，最新版本又提供了web2.0爬虫的支持。

[官方文档](https://github.com/scrapy/scrapy),基本介绍：

* [学习Scrapy入门](http://www.jianshu.com/p/a8aad3bf4dc4)

#### 多线程爬取

> 我们之前写的爬虫都是单个线程的？这怎么够？一旦一个地方卡到不动了，那不就永远等待下去了？为此我们可以使用多线程或者多进程来处理。

参考资料：

* [Python爬虫进阶五之多线程的用法](http://www.cnblogs.com/BigFishFly/p/6380048.html)

#### 验证码识别

对于网站有验证码的情况，我们有三种办法：

- 使用代理，更新IP。
- 使用cookie登陆。
- 验证码识别。

关于验证码识别：

> 可以利用开源的Tesseract-OCR系统进行验证码图片的下载及识别，将识别的字符传到爬虫系统进行模拟登陆。当然也可以将验证码图片上传到打码平台上进行识别。如果不成功，可以再次更新验证码识别，直到成功为止。

#### 分布式爬取

> 分布式爬取，针对比较大型爬虫系统，实现步骤如下所示
> 1.基本的http抓取工具，如scrapy
> 2.避免重复抓取网页，如Bloom Filter
> 3.维护一个所有集群机器能够有效分享的分布式队列
> 4.将分布式队列和Scrapy结合
> 5.后续处理，网页析取（python-goose），存储（Mongodb）

感兴趣的可以参考：

* [纯手工打造简单分布式爬虫](http://www.cnblogs.com/qiyeboy/p/7016540.html)

## 爬取手机贷贴吧数据

**源代码地址:**[爬取手机贷贴吧数据](https://github.com/chenggang0815/python/blob/master/sjd.py)

**主要步骤**

1. 观察列表页URL规则，拼接所有要提取的列表页URL

2. 发现返回的html中含有大量注释符号，于是将html文件中的注释符号替换空格

3. 分别分析标题，作者，发帖时间，帖子回复数的规则。以下分别是上述字段的html节点：

    **标题**

```
<a href="/p/5223773460" title="这边保证全网最低利息，需要的来当天下" target="_blank" class="j_th_tit ">这边保证全网最低利息，需要的来当天下</a>
```

 通过观察发现每个title都在`<a>`节点中，并且**class**属性都等于"j_th_tit "，于是我们可以这样提取：

```
a =s.find_all('a',class_='j_th_tit ')
    for i in a:
title.append(i.string)
```

​      **作者**

```
<span class="tb_icon_author no_icon_author"
          title="主题作者:FUDS"
          data-field='{&quot;user_id&quot;:2407169253}' >
```

这里由于每个title的内容都包含’主题作者‘四个字，这并不是我们想要的，于是可以配合正则表达式这样提取：

```
b = s.find_all('span', title=re.compile('(主题作者.*)'))
    for i in b:
author.append(i.get_text())
```

​     **发帖时间**

```
<span class="pull-right is_show_create_time" title="创建时间">7-15</span>
```

这个与标题的提取方法同理：

```
c = s.find_all('span',class_='pull-right is_show_create_time')
    for i in c:
time_send.append(i.get_text())
```

**接下来讲一些不一样的**

由于要爬取每个帖子里的回复，那么每个帖子的URL该怎么获得呢？还是**通过观察**，随便点进一个帖子里发现它的URL是这样的：`https://tieba.baidu.com/p/5223773460` 于是我们可以猜测`p/5223773460` 是一个类似于这个帖子的ID。然后我们去列表页的源代码搜索这个编号，果然发现了这个：

`<a href="/p/5223773460" title="这边保证全网最低利息，需要的来当天下" target="_blank" class="j_th_tit ">这边保证全网最低利息，需要的来当天下</a>`

原来就在提取标题的节点里，于是我们将它提取出来再拼接成对应的URL，就得到了每个列表里每个帖子的URL。

```
e = s.find_all('a', class_='j_th_tit ')
    for i in e:
tiezi_url.append('https://tieba.baidu.com'+i.get('href'))
```

要对帖子里的内容进行爬取，首先是要观察帖子里每一页回复的URL规律，比如一个帖子的回复有多页，我们发现它的第二页是这样的：`https://tieba.baidu.com/p/5155995012?pn=2` 这与我们最开始拼接列表页的URL是一毛一样的。**唯一不同的地方是，我们需要判断每个帖子有多少页回复。**这里我们可以定义一个函数，它返回的是每个帖子有多少页回复：

```
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
```

**其中，有些广告贴可能已经被删除了，我们需要对这种情况进行判断。**接来下如法炮制，我们就把帖子回复的想要的字段提取出来了！！！

最后，就是**数据的存储与导出**。 在这里我将字段存储成pandas库里的dataframe格式，可以很方便的导出csv文件。当然也可以选择用python连接mysql插入数据。具体请参考这里：[python连接mysql并插入数据](http://www.cnblogs.com/zhangtianyuan/p/6951270.html)



## 推荐资料与参考链接

### 参考链接

* [[python  Python爬虫防封杀方法集合](http://www.cnblogs.com/sdfghj/p/6897604.html)]
* [Python 爬虫进阶?](https://www.zhihu.com/question/35461941)

### 推荐资料

* [一看就明白的爬虫入门讲解：基础理论篇](http://www.csdn.net/article/2015-11-13/2826205)
* [python：BeautifulSoup 模块使用指南](http://www.jianshu.com/p/2b783f7914c6)
* [Python爬虫突破封禁的6种常见方法](http://blog.csdn.net/offbye/article/details/52235139)
* [[Python爬虫入门一之综述](http://cuiqingcai.com/927.html)]
* [[Python爬虫入门二之爬虫基础了解](http://cuiqingcai.com/942.html)]
* [[Python爬虫入门三之Urllib库的基本使用](http://cuiqingcai.com/947.html)]
* [[Python爬虫入门四之Urllib库的高级用法](http://cuiqingcai.com/954.html)]
* [[Python爬虫入门五之URLError异常处理](http://cuiqingcai.com/961.html)]
* [[Python爬虫入门六之Cookie的使用](http://cuiqingcai.com/968.html)]
* [ [Python爬虫入门七之正则表达式](http://cuiqingcai.com/977.html)]
