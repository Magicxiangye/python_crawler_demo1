from datetime import datetime, timedelta#时间戳的库
#Mongo数据库的使用库
from pymongo import MongoClient
#使数据变为序列化
import pickle
#压缩文件的库
import zlib
#把字符串数据以bson形式存储到mongodb
from bson.binary import Binary
import crawler

from classMethod.link_crawler import link_crawler
from classMethod.Alexa_Callback_function import AlexaCallback

#数据库的缓存类

class MongoCache:
    def __init__(self,client=None,expires=timedelta(days=30)):
        #timedelta()设置数据存在时间的函数（MongoDB会定期的清理数据，误差在一分钟以内）
        #client为空的话，使用的是默认的本地数据库(把IP换成localhost也可以)
        self.client = MongoClient("127.0.0.1",27017) if client is None else client
        #设置一个关系数据库
        self.db = self.client.cache
        #数据库的create_time（用的是时间戳的方法）
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    #提取的方法
    def __getitem__(self, url):
        #使用的是url 当作id.对数据库进行提取
        record = self.db.webpage.find_one({'_id': url})
        if record:
            #解压加读取(转换格式)
            return pickle.loads(zlib.decompress(record['result']))
        else:
            #不存在的话抛出异常
            raise KeyError(url + 'does not exist')

    #保存下载的url的方法
    def __setitem__(self, url ,result):
        #url要当唯一值传入id
        record = {'result' : Binary(zlib.compress(pickle.dumps(result))),'timestamp': datetime.utcnow()}
        # 会有重复的存储，唯一的存储的方法是，使用update()使用唯一标识来当id，存在时更新，不存在时插入
        self.db.webpage.update_one({'_id': url},{'$set': record},upsert=True)



#test the method MongoDB(use the same downloadmethods ps:net is the important things )
if __name__ == '__main__':
    #test
    #下载这个网页的回调函数
    scrape_callback = AlexaCallback()
    test_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
    #用的时候把检视爬虫文件的功能去掉，就可以正常的爬取了
    link_crawler(seed_url=test_url, cache=MongoCache(),scrape_callback=scrape_callback)