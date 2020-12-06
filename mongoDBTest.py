from pymongo import MongoClient

if __name__ == '__main__':
    #与本地的mongo数据库建立连接
    client = MongoClient("127.0.0.1",27017)
    print(client)
    url = 'nama'
    testHtml = '...'
    #创建一个缓存
    db = client.cache
    #会有重复的存储，唯一的存储的方法是，使用update()使用唯一标识来当id，存在时更新，不存在时插入
    see = db.webpage.insert_one({'url': url, 'html': testHtml})
    print(see)
    result = db.webpage.find_one({'url': url})
    print(result)