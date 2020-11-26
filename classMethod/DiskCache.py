import os #写入
import re #正则库
import urllib.parse#路径分析

#缓存类
class DiskCache:
    #声明的初始化
    def __init__(self,cache_dir='cache'):
        self.cache_dir = cache_dir
        self.max_length = 255#文件名及其父目录长度需要控制在255个字符之内
    #url转换为保存路径的方法
    def url_to_path(self,url):
        #为url创建一个保存在文件系统的path
        #先用库分解url提取相应的信息
        components = urllib.parse.urlsplit(url)
        #给结尾是空路径的添加上index.html的默认主文件，以便于正常的访问
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        #把其他字符替代掉
        filename = re.sub('[^/0-9a-zA-Z\-.,;_]','_',filename)
        #path 字符长度的限制
        filename = '/'.join(segment[:255] for segment in filename.split('/'))#重新组合一下
        return os.path.join(self.cache_dir,filename)