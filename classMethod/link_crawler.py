import re
import urllib.parse
import time
import datetime
import urllib.robotparser
from classMethod.Downloader import Downloader
from classMethod.ScrapeCallBack_Save import ScrapeCallBack
import chardet   #需要导入这个模块，检测编码格式

User = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
#改进版的link爬虫
def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, user_agent=User, proxies=None,
                 num_retries=1, scrape_callback=None, cache=None):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # 还需要下载的列表
    crawl_queue = [seed_url]
    # 下载的深度（以免碰到下载陷阱）
    seen = {seed_url: 0}
    # 已经下载多少个了
    num_urls = 0
    rp = get_robots(seed_url)
    #初始化一下下载的类
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)

    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        # check url passes robots.txt restrictions
        #先把检测可爬取列表的功能关闭
        if rp.can_fetch(user_agent, url):
            html = D(url)
            links = []
            #回调函数（写入文档.csv文件）
            if scrape_callback:
                # 还得解码编码
                #encode_type = chardet.detect(html)
                #html = html.decode(encoding='gbk')
                links.extend(scrape_callback(url, html) or [])

            if depth != max_depth:
                # can still crawl further
                if link_regex:
                    # 读取robot文件只爬取可以爬取的文件网址
                    # 还得解码编码
                    #encode_type = chardet.detect(html)
                    #html = html.decode(encode_type['encoding'])
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        # check link is within same domain
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)

            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print('Blocked by robots.txt:', url)


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urllib.parse.urldefrag(link)  # remove hash to avoid duplicates
    return urllib.parse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urllib.parse.urlparse(url1).netloc == urllib.parse.urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


if __name__ == '__main__':
    #link_crawler('http://example.webscraping.com', '/(index|places)/(index|default)/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com', '/(index|places)/(index|default)/(index|view)', delay=0, num_retries=1, max_depth=1,
                 user_agent='GoodCrawler')
