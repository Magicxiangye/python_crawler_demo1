#多进程共享的数据库的队列的类函数
#为多进程的共享数据库提供了类方法
from datetime import datetime, timedelta#设置数据的时间戳要用到的库
#py操作MongoDB的库
from pymongo import MongoClient, errors

class MongoQueue:
    #定义了一个url可能的3种状态
    #添加一个新的时候--为outstanding
    #下载的时候--processing
    #下载结束的时候--complete
    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, client=None, timeout=300):
        # client为空的话，使用的是默认的本地数据库(把IP换成localhost也可以)
        self.client = MongoClient("127.0.0.1", 27017) if client is None else client
        self.db = self.client.cache
        self.timeout = timeout

    #检测是否队列中链接的状态是否都为complete
    def __nonzero__(self):
        record = self.db.crawl_queue.find_one({'status': {'$ne': self.COMPLETE}})
        return True if record else False

    #将不存在的url加入下载的队列
    def push(self,url):
        try:
            self.db.crawl_queue.insert({'_id': url, 'status': self.OUTSTANDING})
        except errors.DuplicateKeyError as e:
            #当链接已经存在的时候(接住一下错误)
            pass

    #url取出下载函数
    def pop(self):
        #将队列中status为outstanding的提出下载并将状态改为processing
        record = self.db.crawl_queue.find_and_modify(query={'status': self.OUTSTANDING}, update={'$set': {'status': self.PROCESSING,'timestamp': datetime.now()}})
        if record:
            #当修改了一个url的状态的时候,返回这个url
            return record['_id']
        else:
            #当没有url的状态可以改变的时候
            #检测清除一波下载超时的链接的状态
            self.repair()
            raise KeyError()

    #下载完成的状态更改
    def complete(self, url):
        self.db.crawl_queue.update({'id': url}, {'$set': {'status': self.COMPLETE}})


    def clear(self):
        self.db.crawl_queue.drop()

    #将下载超时的链接暂停
    def repair(self):
        record = self.db.crawl_queue.find_and_modify(query={'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},'status': {'$ne': self.COMPLETE}},
                                                     update={'$set': {'status': self.OUTSTANDING}})
        if record:
            print('结束的url状态是：', record['_id'])
