#下载alexa的保存回调方法
#import 基本的库
import csv
#文件流的格式
import pickle
#压缩的库
from zipfile import ZipFile
#数据流的库
from io import StringIO


class AlexaCallback:
    def __init__(self,max_url=100):
        self.max_url = max_url
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'


    #callback的方法
    def __call__(self,url,html):
        if url == self.seed_url:
            #是种子的网站，可以开始下载解析网页的下载
            urls = []
            #先打开流，下载一下压缩文件包
            with ZipFile(StringIO(html)) as zf:
                #读取解压list中需要的文件的名称
                csv_filename = zf.namelist()[0]#因为这个压缩包只有一个文件
                #只读取csv中的website的数据
                for _,website in csv.reader(zf.open(csv_filename)):
                    print(website)
                    urls.append('http://' + website)
                    if len(urls) == self.max_url:
                        break

            #返回网址的list
            return urls