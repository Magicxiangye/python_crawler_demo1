#多进程的爬虫

import time
import urllib.parse
#多进程的库
import multiprocessing
#下载类的import
from classMethod.Downloader import Downloader
from classMethod.MongoQueue import MongoQueue



#在队列类的内部会处理重复的url，所以不需要再设置一个set来检测是否重复
def process_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None, num_retries=1, max_threads=10, timeout=60):
    # 保存网址的线性表的共享数据库（代替了多进程的只在内部保存的list）
    crawl_queue = MongoQueue()#先设置保存的是本地的数据库
    crawl_queue.clear()
    crawl_queue.push(seed_url)# 还是从初始的网址开始下载
    # 初始化下载
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries)



#把每个网页的具体地址拼接好
def normalize(seed_url, link):
    link, _ = urllib.parse.urldefrag(link)
    result = urllib.parse.urljoin(seed_url, link)
    return result