#多进程的爬虫

import time
import urllib.parse
#多进程的库
import multiprocessing
import time
import threading
#下载类的import
from classMethod.Downloader import Downloader
from classMethod.MongoQueue import MongoQueue


SLEEP_TIME = 1



#在队列类的内部会处理重复的url，所以不需要再设置一个set来检测是否重复
#多线程的方法
def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None, num_retries=1, max_threads=10, timeout=60):
    # 保存网址的线性表的共享数据库（代替了多进程的只在内部保存的list）
    crawl_queue = MongoQueue()#先设置保存的是本地的数据库
    crawl_queue.clear()
    crawl_queue.push(seed_url)# 还是从初始的网址开始下载
    # 初始化下载
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries)

    #多进程的下载函数定义
    def process_queue():
        #下载的步骤还是一样的
        #还是外面嵌套一个循环直到当前没有要下载的任务为止
        while True:
            #还是要接住当有异常的时候
            try:
                url = crawl_queue.pop()
            except KeyError:
                #当前没有要下载的内容
                break
            else:
                #尝试下载
                html = D(url)
                #当有当前网页需要的回调函数的时候
                if scrape_callback:
                    #还是用try的格式
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        #回调函数异常的时候，启动的抓取异常
                        print('Error in callback for: {}: {}'.format(url, e))
                    else:
                        #提取出回调函数返回的下载的列表
                        for link in links:
                            #将每一个地址都加入到MongoDB的queue中去
                            #先把url变为正常的地址
                            norma_link = normalize(seed_url=seed_url, link=link)
                            #push到队列里（加入是数据库的函数会检测是否有重复）
                            crawl_queue.push(norma_link)
                #不管是有回调函数还是没有回调函数
                #只要是下载完了这个url，就要改成complete状态
                crawl_queue.complete(url)

    #多进程活动里的多线程的定义
    #和多线程的一模一样
    threads = []
    while threads or crawl_queue:
        #还是检测失活的线程
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        # 开启线程的操作
        # 当小于最大的线程数且下载list中还有需要下载的文件时将开启线程
        if len(threads) < max_threads and crawl_queue:
            #设置一个新的进程
            thread = threading.Thread(target=process_queue)
            # 设置守护进程， 以便主线程在接收 ctrl - c 时可以退出
            thread.setDaemon(True)
            #开启线程
            thread.start()
            #加入到线程表
            threads.append(thread)

        #休眠(每开启一个线程休眠一下)
        time.sleep(SLEEP_TIME)



#多进程的方法
def process_link_crawler(args, **kwargs):
    #先获取的是电脑cpu的数量
    num_cpus = multiprocessing.cpu_count()
    print('Starting {} processes'.format(num_cpus))#格式化函数的输出
    #多进程的保存
    processes = []
    #有几核的CPU开启几个进程
    for i in range(num_cpus):
        #每个进程又开启多线程
        p = multiprocessing.Process(target=threaded_crawler, args=[args],kwargs=kwargs)
        p.start()
        processes.append(p)

    # join的原理就是依次检验线程池中的线程是否结束，没有结束就阻塞直到线程结束，如果结束则跳转执行下一个线程的join函数。
    #查看所有的进程是否完成
    for p in processes:
        p.join()

#把每个网页的具体地址拼接好
def normalize(seed_url, link):
    link, _ = urllib.parse.urldefrag(link)
    result = urllib.parse.urljoin(seed_url, link)
    return result