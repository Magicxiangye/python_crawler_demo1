# 抽取网页的模块
import lxml.html
# 之前的版本，cssselect直接在lxml中包含了，但是现在作为一个单独的模块出现了。因此需要单独安装。
# import cssselect
from classMethod.Downloader import Downloader

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


# 测试一下动态提取的功能
if __name__ == "__main__":
    # 在爬取动态的网页的时候，没能爬取到当前的动态网页的情况，所以爬取的动态的内容为空
    D = Downloader()
    html = D('http://example.webscraping.com/search')
    # 使用库来结构下载的网页的模型，来提取详细的信息
    tree = lxml.html.fromstring(html)
    result = tree.cssselect('div#results a')
    print(result)