import csv
import re
from bs4 import BeautifulSoup#一个网页的解析模块

#保存数据的回调类
class ScrapeCallBack:
    def __init__(self):
        #初始化表格的格式，表头
        self.writer = csv.writer(open('../countries.csv', 'w'))
        self.fields = ('area','population','iso','country')#需要的文件字段
        self.writer.writerow(self.fields)#第一行当表头

    #使用回调的方法
    def __call__(self, url, html):
        if re.search('/view/',url):
            results = []
            soup = BeautifulSoup(html,"html.parser")
            for field in self.fields:
                results.append(soup.find('table').find('tr', id='places_%s__row' % field).find('td',class_='w2p_fw').text)
            self.writer.writerow(results)

