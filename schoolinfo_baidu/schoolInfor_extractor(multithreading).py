#高校信息抽取器(多线程版)

from InforCollection.headers.UserAgents import get_headers
import requests
from bs4 import BeautifulSoup
import os
import threading
from queue import Queue

#读取学校名称文件
def schoolName_read(filename):
    with open(filename,'r') as f:
        all_schoolName = f.readlines()
    #将学校名称保存为列表
    schoolName = [i.strip() for i in all_schoolName]
    return schoolName

# 生产者
class Producer(threading.Thread):
    headers = {'User-Agent': get_headers()}
    def __init__(self,page_queue,html_queue,infor_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.html_queue = html_queue
        self.infor_queue = infor_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            name,url = self.page_queue.get()
            self.parse_page(name,url)

    def parse_page(self,name,url):

        response = requests.get(url, headers=self.headers)
        # 使用bs4库解析页面
        soup = BeautifulSoup(response.content, 'lxml')
        # 下载网页
        self.schoolPage_save(soup.prettify(), name)

        # 词条属性
        item_attributes = soup.find_all(attrs={'class': 'basicInfo-item name'})
        # 词条属性内容
        item_values = soup.find_all(attrs={'class': 'basicInfo-item value'})
        item_attributeModify = []
        item_valueModify = []
        # 数据清洗(去空格、特定字符)并将修改数据存入列表
        for item_attribute in item_attributes:
            item_attributeModify.append(item_attribute.text.replace(u'\xa0', ''))
        for item_value in item_values:
            item_valueModify.append(item_value.text.replace('\n', '').replace('收起', ''))
        # 使用dict与zip将学校词条打包成字典(映射为 属性：属性值）
        schoolInfor = dict(zip(item_attributeModify, item_valueModify))
        # 将学校信息加入队列
        self.infor_queue.put((name,schoolInfor))

    # 将学校信息页面保存为html文件
    def schoolPage_save(self,data, name):
        page_save_path = './schoolPages/'
        if os.path.exists(page_save_path):
            pass
        else:
            os.mkdir(page_save_path)
        filename = page_save_path + name + '.html'
        self.html_queue.put((data,filename))

class Consumer(threading.Thread):
    def __init__(self,page_queue,html_queue,infor_queue,all_schoolInfor,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.html_queue = html_queue
        self.infor_queue = infor_queue
        self.all_schoolInfor = all_schoolInfor

    def run(self):
        while True:
            if self.page_queue.empty() and self.html_queue.empty() and self.infor_queue.empty():
                break

            #页面下载
            data,filename = self.html_queue.get()
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(data)
            print(filename + ' 下载成功')

            #信息抽取
            name,schoolInfor = self.infor_queue.get()
            self.all_schoolInfor.append(schoolInfor)
            self.schoolInfo_sava('./schoolInfor.txt', self.all_schoolInfor)
            print(name + ' 词条添加成功')

    # 学校信息保存到txt文件中
    def schoolInfo_sava(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(data))
            print("学校信息保存成功")


def main():

    #页面队列
    page_queue = Queue(3000)

    #html队列
    html_queue = Queue(1000)

    #信息队列
    infor_queue = Queue(1000)

    all_schoolInfor = []

    #读取学校名称
    schoolName = schoolName_read('./school_name.txt')
    print('共%d条信息' % len(schoolName))
    for name in schoolName:
        school_url = 'https://baike.baidu.com/item/{}'.format(name)
        #页面队列添加元素,传递(学校名称,url)元组
        page_queue.put((name,school_url))
        print(name + ' 添加队列成功')

    #五个生产者
    for x in range(5):
        t = Producer(page_queue,html_queue,infor_queue)
        t.start()

    #五个消费者
    for x in range(5):
        t = Consumer(page_queue,html_queue,infor_queue,all_schoolInfor)
        t.start()


if __name__ == '__main__':
    main()
