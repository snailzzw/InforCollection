"""豆瓣音乐Top250信息采集（多线程）"""

from InforCollection.headers.UserAgents import get_headers
import requests
from lxml import etree
import re
import threading
from queue import Queue
import pymongo


class DouBanMusicTop250:
    """豆瓣音乐Top250采集类"""

    def __init__(self):
        self.headers = {'User-Agent': get_headers()}
        self.firstUrl = 'https://music.douban.com/top250'
        self.musicQueue = Queue(300)
        self.client = pymongo.MongoClient(host='localhost', port=27017, username='root', password='mongo')['douban']

    def get_response(self, url):
        return requests.get(url, headers=self.headers).content

    def parse_response(self, url):
        content = self.get_response(url)
        html_content = etree.HTML(content)
        music_nodes_list = html_content.xpath('//table')
        for music_node_list in music_nodes_list:
            music_item = dict()
            # 音乐标题
            music_item['music_title_1'] = music_node_list.xpath('.//div[@class="pl2"]/a/text()')[0]
            music_item['music_title_1'] = " ".join(str(music_item['music_title_1']).split())
            music_title_xpath = music_node_list.xpath('.//div[@class="pl2"]/a/span/text()')
            if len(music_title_xpath):
                music_item['music_title_2'] = music_title_xpath[0]
            else:
                music_item['music_title_2'] = ""
            # 音乐图片
            music_item['music_img'] = music_node_list.xpath('.//img/@src')[0]
            # 音乐主要信息
            music_item['music_mainInfor'] = music_node_list.xpath('.//div[@class="pl2"]/p/text()')[0]
            # 音乐评分
            music_item['music_star'] = music_node_list.xpath('.//span[@class="rating_nums"]/text()')[0]
            # 音乐评分人数
            music_fans_xpath = music_node_list.xpath('.//span[@class="pl"]/text()')[0]
            music_item['music_fans'] = re.findall(r'\d+', music_fans_xpath)[0]
            self.musicQueue.put(music_item)
        if url == self.firstUrl:
            return [new_url for new_url in html_content.xpath('//div[@class="paginator"]/a/@href')]

    def run(self):
        url_list = self.parse_response(self.firstUrl)
        thread_list = []
        for url in url_list:
            thread = threading.Thread(target=self.parse_response, args=[url])
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join()
        while not self.musicQueue.empty():
            self.client['music_top250'].insert(self.musicQueue.get())


if __name__ == '__main__':
    douban_music_top250 = DouBanMusicTop250()
    douban_music_top250.run()
