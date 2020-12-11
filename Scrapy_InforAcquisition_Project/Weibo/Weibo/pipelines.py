# -*- coding: utf-8 -*-

import pymongo
from pymongo.errors import DuplicateKeyError
from Weibo.items import TweetsItem, CommentsItem
from Weibo.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, USER, PWD, Data_DB_NAME

class MongoDBPipline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.db_auth = self.client .admin
        self.db_auth.authenticate(USER, PWD)
        self.db = self.client [Data_DB_NAME]

        self.Tweets = self.db['Tweets']
        self.Comments = self.db['Comments']

        # 创建索引
        """
        索引能够实现高效地查询。没有索引，MongoDB 就必须扫描集合中的所有文档，才能找到匹配查询语句的文档。
        这种扫描毫无效率可言，需要处理大量的数据。索引是一种特殊的数据结构，将一小块数据集保存为容易遍历的形式。
        索引能够存储某种特殊字段或字段集的值，并按照索引指定的方式将字段值进行排序
        """
        # self.Tweets.create_index('id', unique=True)
        # self.Comments.create_index('id', unique=True)

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """

        if isinstance(item, TweetsItem):
            self.insert_item(self.Tweets, item)
        elif isinstance(item, CommentsItem):
            self.insert_item(self.Comments, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        # 数据去重
        try:
            collection.insert_one(dict(item))
        except DuplicateKeyError:
            pass

    def close_spider(self, spider):
        self.client.close()

