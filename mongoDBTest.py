from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient("127.0.0.1",27017)
    print(client)
    url = 'nama'
    testHtml = '...'
    db = client.cache
    see = db.webpage.insert_one({'url': url, 'html': testHtml})
    print(see)
    result = db.webpage.find_one({'url': url})
    print(result)