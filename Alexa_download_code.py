#抽取网页的数据的四个步骤
# 1. 下载zip文件
# 2. 从zip文件中提取csv文件
# 3. 解析csv文件
# 4. 遍历csv文件的每一行的，抽取出域名数据(下载网页保存到数据库)

import csv
#提取zip文件的库
from zipfile import ZipFile
#python 3.4以后StringIO和cStringIO就没有了，转移到 io,的StringIO和BytesIO
from io import StringIO
from classMethod.Downloader import Downloader


#start download
D = Downloader()
zipped_data = D('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
urls = []#url 的list
#开始解压(并解析文件)(zipfile 必须要有一个类似于文件接口的东西才可以接收)
with ZipFile(StringIO(zipped_data)) as zf:
    #获取压缩包中csv文件的名字
    csv_filename = zf.namelist()[0]
    for _,website in csv.reader(zf.open(csv_filename)):
        #只需要遍历的网站就可以（其他的就不需要了）
        urls.append('http://' + website)

