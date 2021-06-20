
# 通过QT框架来渲染动态的网页，以得到动态网页的python接口，以获得动态网页的信息
# PyQt使用Qt框架(快速的模拟浏览器的功能)

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# 加载网页web容器
from PyQt5.QtWebKitWidgets import *

# 下载工具的引入
from classMethod.Downloader import Downloader

if __name__ == '__main__':

    url = 'http://example.webscraping.com/dynamic'
    # 创建框架
    # 初始化了QApplication对象，在其他的Qt对象初始化之前
    # Qt框架要先创建这个对象
    app = QApplication([])
    # 这个对象使Web文档的容器
    web = QWebView()
    # 用于创造本地循环事件
    loop = QEventLoop()


