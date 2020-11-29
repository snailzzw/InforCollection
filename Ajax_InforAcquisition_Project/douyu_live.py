"""斗鱼直播（线程池）"""

from InforCollection.headers.UserAgents import get_headers
import requests
import json
import pymongo
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


class DouyuLive:

    def __init__(self):
        self.headers = {'User-Agent': get_headers()}
        # 基础url
        self.baseUrl = 'https://www.douyu.com/gapi/rkc/directory/mixList/0_0/'
        # 第一页
        self.firstUrl = 'https://www.douyu.com/gapi/rkc/directory/mixList/0_0/1'
        # 直播队列
        self.liveQueue = Queue(300)
        # 线程池
        self.executor = ThreadPoolExecutor(max_workers=10)
        # MongoDB对象
        self.client = pymongo.MongoClient(host='localhost', port=27017, username='root', password='mongo')['douyu']

    def get_response(self, url):
        return requests.get(url, headers=self.headers).content

    def parse_response(self, url):
        json_content = json.loads(self.get_response(url))
        json_data = json_content['data']['rl']
        for data in json_data:
            # 直播对象
            live_item = dict()
            # 直播rid
            live_item['live_rid'] = data['rid']
            # 直播标题
            live_item['live_title'] = data['rn']
            # 直播房间名
            live_item['live_roomName'] = data['nn']
            # 直播类型
            live_item['live_type'] = data['c2name']
            # 直播观看数
            live_item['live_fans'] = data['ol']
            # 直播认证
            live_item['live_od'] = data['od']
            # 直播对象入队
            self.liveQueue.put(live_item)
            # 直播对象入库
            self.client['douyu_live'].insert(self.liveQueue.get())
        print('{}解析并入库完成！'.format(url))
        # 如果是第一页，返回页码
        if url == self.firstUrl:
            return json_content['data']['pgcnt']

    def run(self):
        # 提取页码
        last_page_num = self.parse_response(self.firstUrl)
        # url列表
        url_list = [self.baseUrl + str(pg_num) for pg_num in range(1, last_page_num+1)]
        # 线程池
        all_task = [self.executor.submit(self.parse_response, url) for url in url_list]
        # 主线程等待
        wait(all_task, return_when=ALL_COMPLETED)


if __name__ == '__main__':
    douyu_live = DouyuLive()
    douyu_live.run()
