#多线程的连接爬虫下载
import time
import threading
from classMethod.Downloader import Downloader
#线程之间的间隔时间
SLEEP_TIME = 1

#多线程的爬虫
def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None, num_retries=1, max_threads=10, timeout=60):
    #保存网址的线性表
    crawl_queue = [seed_url]#还是从初始的网址开始下载