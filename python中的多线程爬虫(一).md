# Python中的多线程爬虫（一）

最近两周一直在折腾python的多线程爬虫问题，其实也是为了学习python中的面向对象编程以及多线程编程，好在有所收获。那么就来总结一下这两周的知识，等我完全吃透了多线程爬虫，再来写一篇（二），作为多线程的告别篇。

### 线程与进程

进程是什么？可以理解为当你打开一个QQ时，系统就开启了一个进程，而线程永远是包含在进程当中的。比如你用QQ可以同时和多个人聊天，那么就是QQ这个进程同时在执行多个线程，而你如果登录了多个QQ，那就相当于开启了多个进程。下面的这篇文章很形象生动得解释了线程和进程的区别：

* [进程与线程的一个简单解释](http://www.ruanyifeng.com/blog/2013/04/processes_and_threads.html)

### 计算密集型与IO密集型

我们可以把计算机要执行的任务分为计算密集型和IO密集型，那么它们分别代表什么意思呢？

>计算密集型任务的特点是要进行大量的计算，消耗CPU资源，比如计算圆周率、对视频进行高清解码等等，全靠CPU的运算能力。这种计算密集型任务虽然也可以用多任务完成，但是任务越多，花在任务切换的时间就越多，CPU执行任务的效率就越低，所以，要最高效地利用CPU，计算密集型任务同时进行的数量应当等于CPU的核心数。计算密集型任务由于主要消耗CPU资源，因此，代码运行效率至关重要。Python这样的脚本语言运行效率很低，完全不适合计算密集型任务。对于计算密集型任务，最好用C语言编写。
>
>第二种任务的类型是IO密集型，涉及到网络、磁盘IO的任务都是IO密集型任务，这类任务的特点是CPU消耗很少，任务的大部分时间都在等待IO操作完成（因为IO的速度远远低于CPU和内存的速度）。对于IO密集型任务，任务越多，CPU效率越高，但也有一个限度。常见的大部分任务都是IO密集型任务，比如Web应用。IO密集型任务执行期间，99%的时间都花在IO上，花在CPU上的时间很少，因此，用运行速度极快的c语言替换用python这样运行速度极低的脚本语言，完全无法提升运行效率。对于IO密集型任务，最合适的语言就是开发效率最高（代码量最少）的语言，脚本语言是首选，C语言最差。

从上面这段话我们可以看出来，计算密集型，顾名思义，需要消耗大量CPU资源，并且python这样的脚本语言在执行计算密集型任务时并不占优势；而IO密集型任务，可以大意理解为文件写入（Input）/写出（Output），这类任务不怎么消耗CPU资源。那么这两个类型的任务和我们的多线程爬虫到底有什么关系呢？下面就来讲一讲python中的多线程。

### python中的多线程

我看到过很多次诸如“python下的多线程是鸡肋，推荐使用多进程”的话，这句话只能说是半对，为什么呢？

那是因为在python中存在一种叫做GIL（Global Interpreter Lock）全局解释器锁的东西，这玩意儿是python设计之初的考虑，为了数据安全所做的决定。在python的多线程中，运行情况是这样子的：

1.获取GIL

2.执行代码直到sleep或者是python虚拟机将其挂起。

3.释放GIL

**可见，某个线程想要执行，必须先拿到GIL，我们可以把GIL看作是“通行证”，并且在一个python进程中，GIL只有一个。拿不到通行证的线程，就不允许进入CPU执行**

而每次释放GIL锁，线程进行锁竞争、切换线程，会消耗资源。**并且由于GIL锁存在，python里一个进程永远只能同时执行一个线程(拿到GIL的线程才能执行)** ，这就是为什么在多核CPU上，python的多线程效率并不高。这是python中多线程不如其他语言效率高的原因，但是！但是如果对于IO密集型任务而言，多线程能够有效的提高效率（单线程下有IO操作会进行IO等待，造成不必要的时间浪费，而开启多线程能在线程A等待时，自动切换到线程B，可以不浪费CPU的资源，从而能提升程序执行效率）。

### python中的多线程编程

在python有thread和threading这两个模块可以用于多线程编程，但是我们一般只使用threading模块，这是因为threadin模块不仅覆盖了thread的所有功能，还具备一些thread不具备的高级功能。比如：thread模块不支持守护线程，当主线程退出时，所有的子线程不论它们是否还在工作，都会被强行退出。你可能会疑惑什么是守护线程，什么又是主线程。主线程是用来区别于我们建立的子线程的，即如果我们没有使用多线程，那么程序中唯一的线程就是主线程。守护线程是属于子线程的一类，如果你设置某个线程为守护线程，就表示这个线程不是重要的，在子线程结束的时候，不用等待这个线程完成。下面主要来讲一下threading模块，它不仅提供了Thread类，还提供了各种非常好的同步机制。

Thread类的主要函数有：

```python
start() 开始线程的执行
run() 定义线程的功能的函数（一般会被子类重写！）
join(timeout=None) 程序挂起，直到线程结束，如果给了timeout，则最多阻塞timeout秒
getName() 返回线程的名字
setName(name) 设置线程的名字
setDaemon(True) 设置守护线程，一定要在start()函数前调用

```

threading的Thread类是我们主要的运行对象，使用它我们主要有三种方法来创建线程：

- 创建一个Thread的实例，传给它一个函数；
- 创建一个Thread的实例，传递给它一个可调用的类对象
- 从Thread派生出一个子类，创建一个这个子类的实例

**第一种方法，我们先创建一个Thread实例**，再传给它一个函数。（ps：需要有python中的面向对象知识）

```python
from time import sleep,ctime
import threading

loops=[4,2]

def loop(nloop,nsec):
    print('start loop ',nloop,'at:',ctime())
    sleep(nsec)
    print('loop',nloop,'done at:',ctime())

def main():
    print('starting at:',ctime())
    threads=[]
    nloops=range(len(loops))

    for i in nloops:
        t=threading.Thread(target=loop,args=(i,loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all Done at:',ctime())

if __name__ == '__main__':
    main()
```

在上面的例子中，我们初始化了一个Thread对象，把函数及其参数传进去。在线程开始执行的时候，这个函数会被执行。在所有的线程都创建了之后，再一起调用start()函数。再简单的对每个线程调用join()函数，它会等到线程结束或者在超出timeout参数的时候。join()的另外一个好处是它可以完全不用调用，一旦线程启动后，就会一直运行，直到线程的函数结束。

**第二种方法 试试创建一个Thread的实例，并且传给它一个可调用的类对象** 

```python
import threading
from time import sleep,ctime

loops=[4,2]

class ThreadFunc(object):
    def __init__(self,func,args,name=''):
        self.name=name
        self.func=func
        self.args=args

    def run(self):
        self.func(*self.args)

def loop(nloop,nsec):
    print('start loop ', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())

def main():
    print('starting at:',ctime())
    threads=[]
    nloops=range(len(loops))

    for i in nloops:
        t= threading.Thread(target=ThreadFunc(loop,(i,loops[i]),loop.__name__))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all Done at:',ctime())

if __name__ == '__main__':
    main()
```

相对于一个或几个函数来说，由于类对象里可以使用类的强大功能，这种方法更为灵活。我们实例化了两个

对象，我们增加了一个ThreadFunc类，目的是使它在调用什么函数方面尽量地通用，并不局限于那个loop()对象。因此，我们是传了一个可调用的类（的实例），而不是仅传一个函数，这样做更有面向对象的概念。

**第三种方法 从Thread派生出一个子类，创建一个这个子类的实例**

```python
import threading
from time import sleep,ctime

loops=[2,4]

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args

    def run(self):
        self.func(*self.args)

def loop(nloop,nsec):
    print('start loop',nloop,'at:',ctime())
    sleep(nsec)
    print('loop',nloop,'done at',ctime())

def main():
    print('starting at:',ctime())
    threads=[]
    nloops=range(len(loops))

    for i in nloops:
        t=MyThread(loop,(i,loops[i]),loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all Done at:',ctime())

if __name__ == '__main__':
    main()
```

### 	不得不说的queue模块

上面介绍了创建线程的方式，可这与queue又有什么关系呢？它的作用就是用来提供线程同步机制的！！！

这是出于数据的安全性来考虑的，因为不同的线程共享数据，可以会造成数据不同步的惨案发生。而队列先进先出的特性使得线程在对数据进行操作的时候确保数据不会被反复修改。可以把任何数据的操作分解成以下两个操作，数据的放入以及数据的拿出，这两个步骤是完全独立的。而在我们的爬虫中，多个线程分别从queue中将数据取出，可以保证数据的安全性。下面来举个例子：

```python
import queue
myqueue = queue.Queue(maxsize = 10) #创建一个大小为10的队列
myqueue.put(1)#将一个值放入队列
a=myqueue.get()#将值从队列取出
#以下是我们在多线程爬虫中需要用到的一些方法
queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
queue.join() 实际上意味着等到队列为空，再执行别的操作
```

### 多线程爬虫

请听下回分解~

### 附录

* 异步IO

  >考虑到CPU和IO之间巨大的速度差异，一个任务在执行的过程中大部分时间都在等待IO操作，单进程单线程模型会导致别的任务无法并行执行，因此，我们才需要多进程模型或者多线程模型来支持多任务并发执行。
  >
  >现代操作系统对IO操作已经做了巨大的改进，最大的特点就是支持异步IO。如果充分利用操作系统提供的异步IO支持，就可以用单进程单线程模型来执行多任务，这种全新的模型称为事件驱动模型，Nginx就是支持异步IO的Web服务器，它在单核CPU上采用单进程模型就可以高效地支持多任务。在多核CPU上，可以运行多个进程（数量与CPU核心数相同），充分利用多核CPU。由于系统总的进程数量十分有限，因此操作系统调度非常高效。用异步IO编程模型来实现多任务是一个主要的趋势。 

* python下想要充分利用多核，就用多进程

  ​

  >原因是：每个进程有各自独立的GIL，互不干扰，这样就可以真正意义上的并行执行，所以在python中，多进程的执行效率优于多线程(仅仅针对多核CPU而言)。
  >
  >**所以我们能够得出结论：多核下，想做并行提升效率，比较通用的方法是使用多进程，能够有效提高执行效率**。

* 线程同步

  > 有过相关线程编程经验的人都知道一般当**多个线程共用一些数据的时候，我们就需要对这些线程进行同步**，避免多个进程同时修改这些共用数据的时候产生错误。试想：一个线程的工作是将一个数加一，另一个线程的工作是将这个数减一，假设这个数初始值是1，那么当这两个线程同时要对这个数操作，结果呢？结果是不可预知的。因为他们对这个数的操作产生了冲突，而计算机是没法避免这种冲突的。所以我们要在写程序的时候就解决这种可能的错误，我们该怎么办呢？
  >
  >上锁！所谓上锁，就是当一个线程要操作这个数据之前，把通向这个数据的“门”锁上(也就是禁止了其他语句访问这个数据)，然后执行该执行的操作，当这些操作完成了，离开的时候把这个“门”再打开。当门锁上的时候，假如别的线程要操作这个数据，它就会被告知，这门里有人了，你先等着，直到其他线程操作完了，门再次打开以后，它才会继续原本的操作。
  >
  >**Python的Queue库，提供了线程同步机制**(这个机制就类似上面说的上锁的这个流程)，我们可以直接使用queue轻松实现多线程同步。

### 参考链接

* [Python爬虫:初探多线程爬虫](http://blog.csdn.net/u013787595/article/details/49446291)
* [Python爬虫进阶五之多线程的用法](http://cuiqingcai.com/3325.html)
