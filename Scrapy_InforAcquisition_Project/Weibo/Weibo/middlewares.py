# -*- coding: utf-8 -*-

from Weibo.headers.UserAgents import get_headers
import pymongo
import random
from Weibo.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, USER, PWD, Account_DB_NAME


class CookieMiddleware(object):
    """
    Cookie中间件
    每次请求都随机从账号池中选择一个账号去访问
    """

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db_auth = client.admin
        db_auth.authenticate(USER, PWD)
        self.account_collection = client[Account_DB_NAME]['weibo']

    def process_request(self, request, spider):
        all_count = self.account_collection.find({'status': 'success'}).count()
        if all_count == 0:
            raise Exception('当前账号池为空')
        random_index = random.randint(0, all_count - 1)
        random_account = self.account_collection.find({'status': 'success'})[random_index]

        request.headers["User-Agent"] = get_headers()
        request.headers.setdefault('Cookie', random_account['Cookie'])
        request.meta['account'] = random_account


class RedirectMiddleware(object):
    """
    检测账号是否正常
    302 / 403,说明账号cookie失效/账号被封，状态标记为error
    418,偶尔产生,需要再次请求
    """

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db_auth = client.admin
        db_auth.authenticate(USER, PWD)
        self.account_collection = client[Account_DB_NAME]['weibo']

    def process_response(self, request, response, spider):
        http_code = response.status
        if http_code == 302 or http_code == 403:
            self.account_collection.find_one_and_update({'_id': request.meta['account']['_id']},
                                                        {'$set': {'status': 'error'}}, )
            return request
        elif http_code == 418:
            return request
        else:
            return response