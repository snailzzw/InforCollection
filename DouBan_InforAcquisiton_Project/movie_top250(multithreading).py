"""豆瓣电影Top250信息采集（多线程）"""

from InforCollection.headers.UserAgents import get_headers
import requests
from lxml import etree
import re
import threading
from queue import Queue
import pymongo


class DouBanMovieTop250:
    """豆瓣电影Top250采集类"""

    def __init__(self):

        self.headers = {'User-Agent': get_headers()}
        # 首页
        self.firstUrl = 'https://movie.douban.com/top250'
        # 数据队列
        self.movieQueue = Queue(300)
        # MongoDB客户端对象
        self.client = pymongo.MongoClient(host='localhost', port=27017, username='root', password='mongo')['douban']

    def get_response(self, url):
        """发起请求并获取响应"""
        return requests.get(url, headers=self.headers).content

    def parse_response(self, url):
        """解析响应"""
        content = self.get_response(url)
        # 解析页面
        html_content = etree.HTML(content)
        # 所有电影节点
        movie_nodes_list = html_content.xpath('//div[@class="item"]')
        # 遍历节点提取信息
        for movie_node_list in movie_nodes_list:
            # 每部电影信息保存为一部字典
            movie_item = dict()
            # 电影标题
            movie_title_xpath = movie_node_list.xpath('./div[@class="info"]//span[@class="title"]/text()')
            if len(movie_title_xpath) == 2:
                movie_item['movie_title_1'] = movie_title_xpath[0]
                movie_item['movie_title_2'] = str(movie_title_xpath[1]).replace('\xa0/\xa0', '')
            else:
                movie_item['movie_title_1'] = movie_title_xpath[0]
                movie_item['movie_title_2'] = ""
            # 电影其他标题
            movie_other_title_xpath = movie_node_list.xpath('./div[@class="info"]//span[@class="other"]/text()')
            if len(movie_other_title_xpath):
                movie_item['movie_title_other'] = str(movie_other_title_xpath[0]).replace('\xa0/\xa0', '')
            else:
                movie_item['movie_title_other'] = ""
            # 电影链接
            movie_item['movie_href'] = movie_node_list.xpath('.//a/@href')[0]
            # 电影图片
            movie_item['movie_img'] = movie_node_list.xpath('.//img/@src')[0]
            # 电影主要信息
            movie_item['movie_mainInfor'] = movie_node_list.xpath('.//p/text()')[0]
            movie_item['movie_mainInfor'] = " ".join(str(movie_item['movie_mainInfor']).split())
            # 电影评分
            movie_item['movie_star'] = movie_node_list.xpath('.//span[@class="rating_num"]/text()')[0]
            # 电影评分人数,正则表达式提取数字
            movie_fans_xpath = movie_node_list.xpath('.//span[4]/text()')[0]
            movie_item['movie_fans'] = re.findall(r'\d+', movie_fans_xpath)[0]
            # 电影评价
            if len(movie_node_list.xpath('.//span[@class="inq"]/text()')):
                movie_item['movie_quote'] = movie_node_list.xpath('.//span[@class="inq"]/text()')[0]
            else:
                movie_item['movie_quote'] = ""
            # 加入数据队列
            self.movieQueue.put(movie_item)
            # 如果是首页，则返回页面队列,页面拼接
        if url == self.firstUrl:
            return [self.firstUrl + new_url for new_url in html_content.xpath('//div[@class="paginator"]/a/@href')]

    def run(self):
        """开始"""
        # 解析首页，获取页面队列
        url_list = self.parse_response(self.firstUrl)
        # 线程队列
        thread_list = list()
        for url in url_list:
            # 创建线程
            thread = threading.Thread(target=self.parse_response, args=[url])
            # 启动线程
            thread.start()
            # 线程入队
            thread_list.append(thread)
        # 父进程等所有子进程结束后再结束
        for thread in thread_list:
            thread.join()
        # 将队列中的数据插入数据库
        while not self.movieQueue.empty():
            self.client['movie_top250'].insert(self.movieQueue.get())


if __name__ == '__main__':
    douban_movie_top250 = DouBanMovieTop250()
    douban_movie_top250.run()
