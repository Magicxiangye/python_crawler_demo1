from datetime import datetime, timedelta
import os #写入
import re #正则库
import urllib.parse#路径分析
try:
    import cpickle as pickle
except ImportError:
    import _pickle as pickle #序列化过程叫作 pickle，它能够实现任意对象与文本之间的相互转化，也可以实现任意对象与二进制之间的相互转化。也就是说，pickle 可以实现 Python 对象的存储及恢复。
import zlib

# pickle 模块提供了以下 4 个函数供我们使用：
# dumps()：将 Python 中的对象序列化成二进制对象，并返回；
# loads()：读取给定的二进制对象数据，并将其转换为 Python 对象；
# dump()：将 Python 中的对象序列化成二进制对象，并写入文件；
# load()：读取指定的序列化数据文件，并返回对象。


from classMethod.link_crawler import link_crawler
#缓存类
class DiskCache:
    #声明的初始化
    def __init__(self,cache_dir='cache',expires=timedelta(days=30), compress=True):
        self.cache_dir = cache_dir#保存的主文件名
        self.max_length = 255#文件名及其父目录长度需要控制在255个字符之内
        self.expires = expires
        self.compress = compress
    #url转换为保存路径的方法(映射为安全的文件名)
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

    def has_expired(self, timestamp):
        """Return whether this timestamp has expired
        """
        return datetime.utcnow() > timestamp + self.expires
    #根据文件名获取Cache的对象
    def __getitem__(self, url):
        """Load data from disk for this URL
               """
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                print(result,'exist')
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            # url不存在的情况
            raise KeyError(url + ' does not exist')

    #根据文件名来保存cache到本地
    def __setitem__(self,url,result):
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dumps((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)#将 Python 中的对象序列化成二进制对象，并返回




if __name__ =='__main__':
    link_crawler('http://bing.com', '/(index|places)/(index|default)/(index|view)', cache=DiskCache())