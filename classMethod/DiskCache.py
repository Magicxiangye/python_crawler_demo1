import os #写入
import re #正则库
import urllib.parse#路径分析
import pickle #序列化过程叫作 pickle，它能够实现任意对象与文本之间的相互转化，也可以实现任意对象与二进制之间的相互转化。也就是说，pickle 可以实现 Python 对象的存储及恢复。
#缓存类
class DiskCache:
    #声明的初始化
    def __init__(self,cache_dir='cache'):
        self.cache_dir = cache_dir
        self.max_length = 255#文件名及其父目录长度需要控制在255个字符之内
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
    #根据文件名获取Cache的对象
    def __getitem__(self, url):
        path = self.url_to_path(url)
        #判断是否存在于cache中
        if os.path.exists(path):
            with open(path,'rb') as fp:
                return pickle.load(fp)#读取指定的序列化数据文件，并返回对象。
        else:
            #当url不存在于cache中时（抛出一个key的error）
            raise KeyError(url + 'does not exist')

    #根据文件名来保存cache到本地
    def __setitem__(self,url,result):
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(path):
            os.mkdir(folder)
        with open(path,'rb') as fp:
            fp.write(pickle.dumps(result))#将 Python 中的对象序列化成二进制对象，并返回

