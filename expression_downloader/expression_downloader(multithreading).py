# 多线程下载表情

from InforCollection.headers.UserAgents import get_headers
import threading
import requests
from lxml import etree
from urllib.request import urlretrieve
import socket
import os
import re
from queue import Queue

#生产者
class Producer(threading.Thread):
    headers = {'User-Agent': get_headers()}
    #*args代表任意未知参数，**kwargs代表任意关键字参数
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    #队列执行
    def run(self):
        while True:
            #页面队列为空
            if self.page_queue.empty():
                break
           #获取队列中最后一个url
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        # lxml解析网页
        html = etree.HTML(text)
        # 定位所有图片标签
        imgs = html.xpath("//div[@class='page-content text-center']//img")
        # 图片数量
        img_num = len(imgs)

        for img in imgs:
            # 获取某属性值
            img_url = img.get('data-original')
            # 获取图片名称
            alt = img.get('alt')
            # 正则过滤非法字符
            alt = re.sub(r'[\\?<>/|:"*]', '', alt)
            # 获取文件后缀名
            suffix = os.path.splitext(img_url)[1]
            # 构造文件名
            img_name = alt + suffix
            # 图片保存路径
            img_save_path = "./images/"
            if os.path.exists(img_save_path):
                pass
            # 如果目录不存在则创建
            else:
                os.mkdir(img_save_path)
            filename = img_save_path + img_name
            #将图片url和文件名加入图片队列
            self.img_queue.put((img_url,filename))

#消费者
class Consumer(threading.Thread):
    #*args代表任意未知参数，**kwargs代表任意关键字参数
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            #如果两个队列都是空
            if self.page_queue.empty() and self.img_queue.empty():
                break
            #解包
            img_url,filename = self.img_queue.get()
            #下载
            socket.setdefaulttimeout(30)
            # 解决下载不完全问题且避免陷入死循环
            try:
                urlretrieve(img_url, filename)
            except socket.timeout:
                count = 1
                while count <= 5:
                    try:
                        urlretrieve(img_url, filename)
                        break
                    except socket.timeout:
                        err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                        print(err_info)
                        count += 1
                if count > 5:
                    print("download job failed!")
            # img = requests.get(img_url)
            # with open(filename,'wb') as f:
            #     f.write(img.content)
            # request.urlretrieve(img_url, filename)
            print(filename + "下载完成！")

def main():

    #页面队列
    page_queue = Queue(100)
    #图片队列
    img_queue = Queue(1000)

    # 构造url列表
    for x in range(1,101):
        #使用format构造url
        url = "https://www.doutula.com/photo/list/?page={}".format(x)
        #队列添加元素
        page_queue.put(url)

    #五个生产者
    for x in range(5):
        t = Producer(page_queue,img_queue)
        t.start()

    #五个消费者
    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()