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
    def __init__(self,delay=5,user_agent='magicye',proxies=None,num_retries=1,cache=None):
        self.throttle = Throttle(delay) #下载限速
        self.user_agent = user_agent #伪装用户的头
        self.proxies = proxies #代理选项
        self.num_retries = num_retries#重新下载的次数设置
        self.cache = cache#缓存
    def __call__(self,url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                #当url不存在在缓存里
                pass
            #下载错误继续下载的功能(看看能不能成功)
            else:
                if self.num_retries > 0 and \
                    500 < result['code'] < 600:
                    result = None#重新下载

        if result is None:
            #这个url，没有缓存，需要下载然后加入cache列表
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None#没有代理就不用添加
            headers = {'User-agent': self.user_agent}#请求头，字典类型(可以伪装成浏览器)
            result = self.download(url,headers,proxy,self.num_retries)#调用下载方法
            if self.cache:
                #将结果保存在cache中
                self.cache[url] = result
        #返回值
        return result['html']

    #下载方法（不用缓存，简单下载从的话，直接调用这个方法就可以，不用使用__call__函数来使用这个方法）
    def download(self,url,headers,proxy,num_retries,data=None):
        code = None
        print('Downloading:', url)
        request = urllib.request.Request(url, headers=headers)
        # 当有代理时检查代理
        opener = urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}  # url协议有默认的,没有的话加上--像'http'
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            html = urllib.request.urlopen(request).read()
        except urllib.error.HTTPError as e:
            print('Download error', e.reason)
            html = None
            code = e.code
            if num_retries > 0:
                if hasattr(e,'code') and 500 <= e.code < 600:
                    #返回5xx的HTTP错误重新下载试试
                    return self.download(url,headers,proxy,num_retries-1)

        return {'html':html,'code':code}#注意输出变成了字典（要提取一下）



