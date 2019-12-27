# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

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

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            #获取在settings中定义的变量
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
