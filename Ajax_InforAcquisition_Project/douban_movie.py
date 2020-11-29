"""豆瓣电影（选电影）"""

from InforCollection.headers.UserAgents import get_headers
import requests
import json
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import pymongo


class DoubanMovie:
    def __init__(self):
        self.headers = {'User-Agent': get_headers()}
        self.baseUrl = 'https://movie.douban.com/j/search_subjects?' \
                       'type=movie&tag=热门&sort=rank&page_limit=10&page_start={}'
        self.startPg = 0
        self.movieQueue = Queue(300)
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.client = pymongo.MongoClient(host='localhost', port=27017, username='root', password='mongo')['douban']

    def get_response(self, url):
        return requests.get(url, headers=self.headers).content

    def parse_response(self, url):
        json_content = json.loads(self.get_response(url))
        json_data = json_content['subjects']
        if json_data:
            for data in json_data:
                # 电影对象
                movie_item = dict()
                # 电影id
                movie_item['movie_id'] = data['id']
                # 电影标题
                movie_item['movie_title'] = data['title']
                # 电影链接
                movie_item['movie_url'] = data['url']
                # 电影封面
                movie_item['movie_cover'] = data['cover']
                # 电影评分
                movie_item['movie_rate'] = data['rate']
                # 电影对象入队
                self.movieQueue.put(movie_item)
                # 电影对象入库
                self.client['douban_movie'].insert(self.movieQueue.get())
            print('{}解析成功并入库！'.format(url))
        else:
            print('{}无数据！'.format(url))

    def run(self):
        # url队列
        url_list = [self.baseUrl.format(pg_num) for pg_num in range(10, 1001, 10)]
        # 线程池
        all_task = [self.executor.submit(self.parse_response, url) for url in url_list]
        # 主线程等待
        wait(all_task, return_when=ALL_COMPLETED)


if __name__ == '__main__':
    douban_movie = DoubanMovie()
    douban_movie.run()
