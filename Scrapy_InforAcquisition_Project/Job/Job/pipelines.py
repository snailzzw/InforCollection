# -*- coding: utf-8 -*-

import pymongo
from pymongo.errors import DuplicateKeyError
from Job.items import TencentJobItem
from Job.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME, USER, PWD


class MongoDBPipline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db_auth = client.admin
        db_auth.authenticate(USER, PWD)
        db = client[DB_NAME]
        self.job = db['tencent_job']

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, TencentJobItem):
            self.insert_item(self.job, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            # insert_one去重（提高效率）
            collection.insert_one(dict(item))
        except DuplicateKeyError:
            """有重复数据"""
            pass
