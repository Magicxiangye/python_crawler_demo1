#集成一个下载用的类，（添加缓存的支持）将下载限速嵌入到下载的类中
import random
import urllib.request#python2.7里urllib2拆分的两个库使用
import urllib.error
import re #分析正则库
import chardet   #需要导入这个模块，检测编码格式
import itertools #操作迭代对象的函数
import urllib.parse #来创建url的绝对路径（url的解析，合并，编码，解码）
import urllib.robotparser #还是python3的独特拆分
from classMethod.Throttle import Throttle

class Downloader:
    #默认的设置
    def __init__(self,delay=5,user_agent='magicye',proxies=None,num_retries=2,cache=None):
        self.throttle = Throttle(delay) #下载限速
        self.user_agent = user_agent #伪装用户的头
        self.proxies = proxies #代理选项
        self.num_retries = num_retries
        self.cache = cache
    def __call__(self,url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                #当url不存在在缓存里
                pass
            #连续下载的功能没有写上

        if result is None:
            #这个url，没有缓存，需要下载然后加入cache列表
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None#没有代理就不用添加
            headers = {'User-agent': self.user_agent}#请求头，字典类型(可以伪装成浏览器)

    #下载方法
    def download(self,url,headers,proxy,data):
        pass




