#多线程的连接爬虫下载(爬虫是存储在本地的内存中的，不同的进程无法进行协同的处理，接下来有多进程的版本)
import time
import threading
from classMethod.Downloader import Downloader
import urllib.parse
#线程之间的间隔时间
SLEEP_TIME = 1

#多线程的爬虫
def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None, num_retries=1, max_threads=10, timeout=60):
    #保存网址的线性表
    crawl_queue = [seed_url]#还是从初始的网址开始下载
    #设置已经存在的set来检索是否需要下载目前的url
    seen = set([seed_url])
    #初始化下载
    D  = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries)

    #多线程的下载过程的函数
    def process_queue():
        #直到所有的网页都下载好，while循环才会停止
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                #说明要下载的所有网页都已经下载好了
                break
            else:
                #使用下载方法进行下载
                html = D(url)
                #下面是查看对应的网页爬虫有没有需要的回调方法
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e :
                        print("error is in callback Function{},{}".format(url, e))
                    else:
                        for link in links:
                            #一个链接一个链接的来还原
                            link = normalize(seed_url, link)
                            #最后看看是否再已存在的列表里
                            if link not in seen:
                                seen.add(link)
                                #下载列表也要添加上
                                crawl_queue.append(link)

    #多线程活动的定义
    threads = []
    while threads or crawl_queue:
        #crawl还是继续的活动
        #当线程表里有线程的时候，要检测是否是活跃的
        for thread in threads:
            #清除一下不活跃的线程
            if not thread.is_alive():
                threads.remove(thread)
        #开启线程的操作
        #当小于最大的线程数且下载list中还有需要下载的文件时将开启线程
        while len(threads) < max_threads and crawl_queue:
            #将设置一个新的线程
            thread = threading.Thread(target=process_queue)
            #设置守护进程， 以便主线程在接收 ctrl - c 时可以退出
            thread.setDaemon(True)
            #开启线程
            thread.start()
            #添加到线程表
            threads.append(thread)
        #每开启一个线程，就休眠一段时间
        time.sleep(SLEEP_TIME)




#把每个网页的具体地址拼接好
def normalize(seed_url, link):
    link, _ = urllib.parse.urldefrag(link)
    result = urllib.parse.urljoin(seed_url, link)
    return result

