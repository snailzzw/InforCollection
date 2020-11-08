# 单线程同步下载表情

from InforCollection.headers.UserAgents import get_headers
import requests
from lxml import etree
from urllib import request
import os
import re

# 解析url
def parse_page(url,page_num):
    #构造headers
    headers = {'User-Agent': get_headers()}
    response = requests.get(url,headers=headers)
    text = response.text
    #lxml解析网页
    html = etree.HTML(text)
    #定位所有图片标签
    imgs = html.xpath("//div[@class='page-content text-center']//img")
    # 图片数量
    img_num = len(imgs)
    print("第%d页共有%d张图片" % (page_num,img_num))
    i=1
    for img in imgs:
        #获取某属性值
        img_url = img.get('data-original')
        #获取图片名称
        alt = img.get('alt')
        # 正则过滤非法字符
        alt = re.sub(r'[\\?<>/|:"*]','',alt)
        #获取文件后缀名
        suffix = os.path.splitext(img_url)[1]
        # 构造文件名
        img_name = alt + suffix
        #图片保存路径
        img_save_path = "./images/"
        if os.path.exists(img_save_path):
            pass
        #如果目录不存在则创建
        else:
            os.mkdir(img_save_path)
        filename = img_save_path + img_name
        # 下载页面的图片
        img = requests.get(img_url)
        with open(filename,'wb') as f:
            f.write(img.content)
        request.urlretrieve(img_url, filename)
        print("第%d页第%d张图片下载成功！" % (page_num,i))
        i += 1

def main():

    # 构造url列表
    for x in range(1,11):
        # 使用format构造url
        url = "https://www.doutula.com/photo/list/?page={}".format(x)
        print("正在解析第%d页" % x)
        parse_page(url,x)
        print("第%d页下载成功！" % x)

# 程序入口
if __name__ == '__main__':
    main()