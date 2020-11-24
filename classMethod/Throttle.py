#在两次下载中添加时延
import urllib.parse
import datetime
import time

#记录每个域名上次访问的时间（给下载限速）
class Throttle:

    def __init__(self,delay):
        #设置两次下载的时延
        self.delay = delay
        #记录时间
        self.domain = {}

    def wait(self,url):
        domain = urllib.parse.urlparse(url).netloc#获取当前url的标识，在字典里搜索相应的上次的访问时间
        last_accessed = self.domain.get(domain)

        if self.delay > 0 and last_accessed is not None :
            #判定具体要时延的时间（可能两次下载的时间间隔就已经超过时延要求的时间了，就不用时延了）
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0 :
                #还需要时延的，进入休眠
                time.sleep(sleep_secs)
        #更新一下这次访问的url的最新的时间
        self.domain[domain] = datetime.datetime.now()
