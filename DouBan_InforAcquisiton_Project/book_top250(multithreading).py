"""豆瓣图书信息采集（多线程）"""

from InforCollection.headers.UserAgents import get_headers
import requests
from lxml import etree
import re
import threading
from queue import Queue
import pymongo


class DouBanBookTop250:
    """豆瓣图书Top250采集类"""

    def __init__(self):
        self.headers = {'User-Agent': get_headers()}
        self.firstUrl = 'https://book.douban.com/top250'
        self.bookQueue = Queue(300)
        self.client = pymongo.MongoClient(host='localhost', port=27017, username='root', password='mongo')['douban']

    def get_response(self, url):
        return requests.get(url, headers=self.headers).content

    def parse_response(self, url):
        content = self.get_response(url)
        html_content = etree.HTML(content)
        book_nodes_list = html_content.xpath('//table')
        for book_node_list in book_nodes_list:
            book_item = dict()
            # 书籍标题
            book_item['book_title'] = book_node_list.xpath('.//div[@class="pl2"]/a/@title')[0]
            # 书籍图片
            book_item['book_img'] = book_node_list.xpath('.//img/@src')[0]
            # 书籍主要信息
            book_item['book_mainInfor'] = book_node_list.xpath('.//p[@class="pl"]/text()')[0]
            # 书籍评分
            book_item['book_star'] = book_node_list.xpath('.//span[@class="rating_nums"]/text()')[0]
            # 书籍评分人数
            book_fans_xpath = book_node_list.xpath('.//span[@class="pl"]/text()')[0]
            book_item['book_fans'] = re.findall(r'\d+', book_fans_xpath)[0]
            # 书籍评价
            book_quote_xpath = book_node_list.xpath('.//span[@class="inq"]/text()')
            if len(book_quote_xpath):
                book_item['book_quote'] = book_quote_xpath[0]
            else:
                book_item['book_quote'] = ""
            print(book_item)
            self.bookQueue.put(book_item)
        if url == self.firstUrl:
            return [new_url for new_url in html_content.xpath('//div[@class="paginator"]/a/@href')]

    def run(self):
        url_list = self.parse_response(self.firstUrl)
        # 线程队列
        thread_list = list()
        for url in url_list:
            # 创建线程
            thread = threading.Thread(target=self.parse_response, args=[url])
            # 线程启动
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join()
        while not self.bookQueue.empty():
            self.client['book_top250'].insert(self.bookQueue.get())


if __name__ == '__main__':
    douban_book_top250 = DouBanBookTop250()
    douban_book_top250.run()
