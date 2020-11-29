"""高校信息抽取器(多线程版)"""

from InforCollection.headers.UserAgents import get_headers
import requests
from bs4 import BeautifulSoup
import os
import threading
from queue import Queue
import pymongo


class Producer(threading.Thread):
    """生产者"""
    def __init__(self, page_queue, html_queue, school_infor_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        threading.Thread.__init__(self)
        self.headers = {'User-Agent': get_headers()}
        self.page_queue = page_queue
        self.html_queue = html_queue
        self.schoolInforQueue = school_infor_queue

    def save_school_page(self, data, name):
        """html页面下载"""
        page_save_path = './schoolPages/'
        if os.path.exists(page_save_path):
            pass
        else:
            os.mkdir(page_save_path)
        filename = page_save_path + name + '.html'
        self.html_queue.put((data, filename))

    def get_response(self, url):
        return requests.get(url, headers=self.headers).content

    def parse_page(self, name, url):
        """页面解析"""
        content = self.get_response(url)
        # 使用bs4库解析页面
        soup = BeautifulSoup(content, 'lxml')
        # 下载网页
        self.save_school_page(soup.prettify(), name)

        # 词条属性
        item_attributes = soup.find_all(attrs={'class': 'basicInfo-item name'})
        # 词条属性内容
        item_values = soup.find_all(attrs={'class': 'basicInfo-item value'})
        item_attribute_modify = []
        item_value_modify = []
        # 数据清洗(去空格、特定字符)并将修改数据存入列表
        for item_attribute in item_attributes:
            item_attribute_modify.append(item_attribute.text.replace(u'\xa0', ''))
        for item_value in item_values:
            item_value_modify.append(item_value.text.replace('\n', '').replace('收起', ''))
        # 使用dict与zip将学校词条打包成字典(映射为 属性：属性值）
        school_infor = dict(zip(item_attribute_modify, item_value_modify))
        # 将学校信息加入队列
        self.schoolInforQueue.put((name, school_infor))

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            # 解包
            name, url = self.page_queue.get()
            self.parse_page(name, url)


class Consumer(threading.Thread):
    """消费者"""
    def __init__(self, page_queue, html_queue, school_infor_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        threading.Thread.__init__(self)
        self.page_queue = page_queue
        self.html_queue = html_queue
        self.schoolInforQueue = school_infor_queue
        self.client = pymongo.MongoClient(host='localhost', port=27017, username='root', password='mongo')['baidu']

    def run(self):
        while True:
            if self.page_queue.empty() and self.html_queue.empty() and self.schoolInforQueue.empty():
                break

            # 页面下载
            data, filename = self.html_queue.get()
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(data)
            print(filename + ' 下载成功')

            # 学校信息入库
            name, school_infor = self.schoolInforQueue.get()
            self.client['baike_schoolInfor'].insert(school_infor)
            print(name + ' 词条添加成功')


class SchoolInforExtractor:
    def __init__(self):
        # 基础url
        self.baseUrl = 'https://baike.baidu.com/item/{}'
        # 页面队列
        self.page_queue = Queue(3000)
        # html队列
        self.html_queue = Queue(1000)
        # 信息队列
        self.schoolInforQueue = Queue(1000)

    @staticmethod
    def read_school_name(filename):
        with open(filename, 'r') as f:
            all_school_name = f.readlines()
        # 将学校名称保存为列表
        school_name = [i.strip() for i in all_school_name]
        return school_name

    def run(self):
        school_name_list = self.read_school_name('./school_name.txt')
        for school_name in school_name_list:
            current_url = self.baseUrl.format(school_name)
            # 页面入队,参数为(学校名称,url)元组
            self.page_queue.put((school_name, current_url))
            print(school_name + ' 添加队列成功')
        # 三个生产者
        for x in range(3):
            t = Producer(self.page_queue, self.html_queue, self.schoolInforQueue)
            t.start()

        # 七个消费者
        for x in range(7):
            t = Consumer(self.page_queue, self.html_queue, self.schoolInforQueue)
            t.start()


if __name__ == '__main__':
    school_infor_extractor = SchoolInforExtractor()
    school_infor_extractor.run()
