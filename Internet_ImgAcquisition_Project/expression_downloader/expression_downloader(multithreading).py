"""表情包下载器（多线程）"""

from InforCollection.headers.UserAgents import get_headers
import requests
from lxml import etree
import re
import os
import threading
from queue import Queue


class Producer(threading.Thread):
    """生产者"""
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer).__init__(*args, **kwargs)
        threading.Thread.__init__(self)
        self.headers = {'User-Agent': get_headers()}
        self.page_queue = page_queue
        self.img_queue = img_queue

    def get_response(self, url):
        return requests.get(url, headers=self.headers).content

    def parse_response(self, url):
        content = self.get_response(url)
        html_content = etree.HTML(content)
        # 全部图片节点
        img_nodes_list = html_content.xpath('//div[@class="page-content text-center"]//img')
        for img_node_list in img_nodes_list:
            # 图片地址
            img_url = img_node_list.get('data-original')
            # 图片名称
            img_alt = img_node_list.get('alt')
            # 过滤非法字符
            img_alt = re.sub(r'[\\?<>/|:"*]', '', img_alt)
            # 提取后缀名
            img_suffix = os.path.splitext(img_url)[1]
            # 图片名字拼接
            img_name = img_alt + img_suffix
            # 图片保存根路径
            img_save_path = './images/'
            if os.path.exists(img_save_path):
                pass
            else:
                os.mkdir(img_save_path)
            # 图片文件名拼接
            img_file_name = img_save_path + img_name
            # 将url和文件名入队
            self.img_queue.put((img_file_name, img_url))

    def run(self):
        """队列执行"""
        while not self.page_queue.empty():
            self.parse_response(self.page_queue.get())


class Consumer(threading.Thread):
    """消费者"""
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer).__init__(*args, **kwargs)
        threading.Thread.__init__(self)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            # 解包
            img_file_name, img_url = self.img_queue.get()
            # 下载图片到本地
            img_downloading = requests.get(img_url)
            with open(img_file_name, 'wb') as f:
                f.write(img_downloading.content)


class ExpressionDownloader:
    """表情下载类"""
    def __init__(self):
        # 页面队列
        self.page_queue = Queue(300)
        # 图片队列
        self.img_quque = Queue(300)
        # 基础url
        self.baseUrl = 'https://www.doutula.com/photo/list/?page={}'
        # 页码数
        self.pageNum = 10

    def run(self):
        # 构造url
        for pg_num in range(1, self.pageNum+1):
            current_url = self.baseUrl.format(pg_num)
            # url入队
            self.page_queue.put(current_url)
        # 三个生产者
        for x in range(3):
            t = Producer(self.page_queue, self.img_quque)
            t.start()
        # 三个消费者
        for x in range(3):
            t = Consumer(self.page_queue, self.img_quque)
            t.start()


if __name__ == '__main__':
    expression_downloader = ExpressionDownloader()
    expression_downloader.run()
