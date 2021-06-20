# 抽取网页的模块
import lxml.html
# 之前的版本，cssselect直接在lxml中包含了，但是现在作为一个单独的模块出现了。因此需要单独安装。=

import json
import string
# import cssselect
from classMethod.Downloader import Downloader

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


# 测试一下动态提取的功能
#  了解网页是如何加载数据的（这个过程被称为逆向工程）
if __name__ == "__main__":
    # 在爬取动态的网页的时候，没能爬取到当前的动态网页的情况，所以爬取的动态的内容为空
    D = Downloader()
    # 下面下载的是带有AJAX的网页反馈的内容
    # html = D('http://example.webscraping.com/ajax/search.json?page=0&page_size=10&search_term=a')
    # 在这个网页的下载中，使用的是ajax连接的搜索
    # page应该表示的是ajax库里总的页数
    # 搜索的结果还会被分为多个页面
    # 具体的网页的搜索的条件，是根据不同的网页来进行调整的
    # 分为多少页是与page_size的大小有关系
    # ajax响应返回的数据是JSON格式的，可以用
    # python的JSON模块解析成为一个字典
    # final_result = json.load(html)
    # 使用库来结构下载的网页的模型，来提取详细的信息
    # tree = lxml.html.fromstring(html)
    # result = tree.cssselect('div#results a')
    # print(final_result)

    # 动态的搜索动态网页的所有的查询结果
    # 格式化的网页模板 format()的填充方式
    template_url = 'http://example.webscraping.com/ajax/search.json?page={}&page_size=10&search_term={}'
    contries = set()
    # 这个网页，每一个字母就是一个搜索的条件
    for letter in string.ascii_lowercase:
        page = 0
        while True:
            html = D(template_url.format(page, letter))
            try:
                # 下载返回的是JSON格式的数据
                ajax = json.load(html)
            except ValueError as e:
                print(e)
                ajax = None
            else:
                for record in ajax['records']:
                    # 加入字典一下，是为了去掉重复
                    contries.add(record['country'])

            page += 1
            if ajax is None or page >= ajax['num_pages']:
                break

    # 生成的数据进行保存
    open('countries.txt', 'w').write('\n'.join(sorted(contries)))
    # 使用的边界条件，也可以更高效的继续宁查询，像是page_size提高显示的数量，也可以使得下载的次数减少
    # 像是匹配的搜索的条件search_term使用正则表达式进行的搜索条件，可以不用进行循环
    # 看网页的情况而定

    # 也可以按行写入CSV文件中


