import urllib.request#python2.7里urllib2拆分的两个库使用
import urllib.error
import re #分析正则库
import chardet   #需要导入这个模块，检测编码格式
import itertools #操作迭代对象的函数
import urllib.parse #来创建url的绝对路径（url的解析，合并，编码，解码）
import urllib.robotparser #还是python3的独特拆分
import builtwith

# 从str到bytes:调用方法encode().
# 编码是把Unicode字符串以各种方式编码成为机器能读懂的ASCII字符串
# 从bytes到str:调用方法decode().

# python3中Unicode字符串是默认格式（就是str类型），
# ASCII编码的字符串（就是bytes类型，bytes类型是包含字节值，其实不算是字符串，python3还有bytearray字节数组类型）要在前面加操作符b或B；
# python2中则是相反的，ASCII编码字符串是默认，Unicode字符串要在前面加操作符u或U
#encode和decode分别指编码和解码。

#网页爬取下载(网页的下载函数)（没有重复下载的机制，遇到错误多试几次）#加入了可以使用代理的选项
def download(url,user_agent='magicye',proxy=None,num_retries=2):
    print('Downloading:',url)
    headers = {'User-agent': user_agent}#请求头，字典类型(可以伪装成浏览器)
    request = urllib.request.Request(url,headers=headers)
    #当有代理时检查代理
    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}#url协议有默认的,没有的话加上--像'http'
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.error.URLError as e:
        print('Download error',e.reason)
        html = None

    return html

#网站地址爬虫
def crawl_sitemap(url):
    #先下载网页
    sitemap = download(url)
    #解码(python3的编码转换)
    encode_type = chardet.detect(sitemap)
    sitemap = sitemap.decode(encode_type['encoding'])#encode_type里的类型换成gbk格式的也可以转化为bytes类型
    #用正则表达式分析链接
    links = re.findall('<loc>(.*?)</loc>', sitemap)#re正则表达式
    #下载获取到的URL
    for link in links:
        html = download(link)
        print(html)

#遍历ID下载的爬虫
def idDownload():
    #itertools的count()创造无限迭代的函数根本停不下来只能按ctrl+c
    max_error = 5 #最大的错误下载次数
    num_error = 0 #当前到的错误次数
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-%d' %page
        html = download(url)
        print(html)
        if html is None:
            num_error +=1
            if num_error == max_error:
                break
        else:
            #只要能下载就重置
            num_error = 0

#通过正则表达式来获取相对应的网页links
def get_links(html):
    #返回从html中读取的link的list
    #使用正则来确定要获取的link
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    #返回相对应的list
    return webpage_regex.findall(html)

#链接爬虫
def link_crawler(seed_url,link_regex,user_agent='GoodCrawler',max_depth =-2):#有的时候代理名要换(爬虫陷阱功能要禁用的话，max_depth为负数就可以)
    crawl_queue = [seed_url]
    print(crawl_queue)
    #使用set表来计入无重复值的表单
    seen = set(crawl_queue)
    depth_dict = {}
    depth_dict[seed_url] = 0
    while crawl_queue:
        url = crawl_queue.pop()
        depth = depth_dict[url]
        #检查robotparser文件只爬取可以爬的文件
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url('http://example.webscraping.com/robots.txt')#设置要阅读的可爬取文件路径（绝对路径）
        rp.read()#开始robots解析
        if rp.can_fetch(user_agent,url):
            html = download(url)
            #还得解码编码
            encode_type = chardet.detect(html)
            html = html.decode(encode_type['encoding'])
            if depth != max_depth:
                for link in get_links(html):
                    if re.match(link_regex, link):
                        link = urllib.parse.urljoin(seed_url, link)  # urljoin将不完整链接拼接
                        if link not in seen:
                            seen.add(link)
                            depth_dict[link] = depth + 1
                            crawl_queue.append(link)
        else:
            print("can not download")

    return crawl_queue



if __name__ == '__main__':
   url = 'http://example.webscraping.com'
   link_regex = '/(index|places)/(index|default)/(index|view)'#地址后缀要写对
   test = link_crawler(url,link_regex)
   print(test)

