# 使用的是Scrapy框架来进行book网页的书籍爬取

import scrapy

import os
import sys


# sys.path.append(r"E:\PycharmProject\python_crawler_demo1\scrapyModel\scrapyModel")
current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

from scrapyModel.items import BookItem

# 继承scrapy.Spider
class BookSpider(scrapy.Spider):
    # 每一个爬虫的唯一标志
    # 一个项目有多个爬虫，name为这个爬虫在这个项目中的唯一的标识
    # 用于在shell中启动自己写的爬虫，这个就是爬虫名

    # 使用的方法
    # scrapy crawl books -o books.csv
    name = "books"

    # 定义爬虫的起点，起点可以为多个，这里只有一个起点
    start_urls = ['http://books.toscrape.com/']

    # 分解
    # 下载完起始的页面后，回调一个页面的解析的函数，默认为parse()
    # 这个解析函数通常用于
    # 1.提取页面中想要的信息（使用的是xPath或CSS选择器）
    # 提取页面中的链接，同时对链接实现下载的请求
    # 页面解析函数通常被实现成一个生成器函数，
    # 每一项从页面中提 取的数据以及每一个对链接页面的下载请求
    # 都由yield语句提交给 Scrapy引擎。
    def parse(self, response):
        # 提取数据
        # 每一本书的信息在<article class="product_pod">中，我们使用
        # css()方法找到所有这样的 article 元素，并依次迭代
        for book in response.css('article.product_pod'):
            name = book.xpath('./h3/a/@title').extract_first()
            price = book.css('p.price_color::text').extract_first()
            yield {
                'name': name,
                'price': price,
            }

        # 提取链接
        # 下一页的 url 在 ul.pager > li.next > a 里面
        # 例如：<li class="next"><a href="catelogue/page-2.html">next</a><li>
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            # 如果找到下一页的 URL，得到绝对路径，构造新的 Request 对象
            next_url = response.urljoin(next_url)
            # request Header参数：http的请求头
            yield scrapy.Request(next_url, callback=self.parse)
