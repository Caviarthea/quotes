# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

#定义第一个pipeline，用于处理数据
class TextPipeline(object):
    def __init__(self):
        #在构造函数中定义text长度限制为50
        self.limit = 50



    def process_item(self, item, spider):
        #首先判断Item是否存在，存在则返回，不存在则抛出DropItem异常
        if item['text']:
            if len(item['text']) > self.limit:
                #运用切片，去除大于50个的字符，然后用restrip()方法来去除字符串末尾指定字符（空格），最后加上"..."
                item['text'] = item['text'][0:self.limit].restrip()+'...'
            return item
        else:
            return DropItem("Missing Text")

#定义第二个pipeline，用于存储数据，连接Mongodb
class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    #类方法from_crawler用来获取setting中的参数
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            #获取在settings中定义的配置信息
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    #当spider启动时启动数据库
    def open_spider(self, spider):
        #使用Pymongo连接Mongod
        self.client = pymongo.MongoClient(self.mongo_uri)
        #再连接MongoDB数据库
        self.db = self.client[self.mongo_db]

    #进行了数据的插入操作
    def process_item(self, item, spider):
        name = item._class_._name_
        self.db[name].insert(dict(item))
        return  item

    #当spider关闭时，关闭数据库
    def close_spider(self, spider):
        self.client.close()

