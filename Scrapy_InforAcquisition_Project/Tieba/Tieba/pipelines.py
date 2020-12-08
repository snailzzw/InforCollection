# -*- coding: utf-8 -*-

import pymongo
from pymongo.errors import DuplicateKeyError
from Tieba.items import MainPostItem, ReplyPostItem
from Tieba.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME, USER, PWD


class MongoDBPipline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db_auth = client.admin
        db_auth.authenticate(USER, PWD)
        db = client[DB_NAME]
        # 主题贴
        self.mainPost = db['main_post']
        # 回复贴
        self.replyPost = db['reply_post']

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        # 如果是主题贴
        if isinstance(item, MainPostItem):
            self.insert_item(self.mainPost, item)

        # 如果是回复贴
        elif isinstance(item, ReplyPostItem):
            self.insert_item(self.replyPost, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            # insert_one去重（提高效率）
            collection.insert_one(dict(item))
        except DuplicateKeyError:
            """有重复数据"""
            pass