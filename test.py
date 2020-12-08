#下载alexa的保存回调方法
#import 基本的库
import csv
#文件流的格式
import pickle
#压缩的库
from zipfile import ZipFile
#数据流的库
from io import StringIO
from io import BytesIO


if __name__ == '__main__':
    i = 0
    with ZipFile('top-1m.csv.zip') as zf:
        csv_filename = zf.namelist()[0]
        print(csv_filename)
        with open('top-1m.csv','r') as file:
            #print(file)
            for _,website in csv.reader(file):
                print(website)
                i = i + 1
                if i == 10:
                    break
