"""表情包下载器（同步）"""

from InforCollection.headers.UserAgents import get_headers
import requests
from lxml import etree
import re
import os


class ExpressionDownloader:

    def __init__(self):
        self.headers = {'User-Agent': get_headers()}
        # 基础url
        self.baseUrl = 'https://www.doutula.com/photo/list/?page={}'
        # 页数
        self.pageNum = 10

    def get_response(self, url):
        return requests.get(url, headers=self.headers).content

    def parse_response(self, url):
        content = self.get_response(url)
        html_content = etree.HTML(content)
        # 所有图片标签
        img_nodes_list = html_content.xpath('//div[@class="page-content text-center"]//img')
        for img_node_list in img_nodes_list:
            # 图片url
            img_url = img_node_list.get('data-original')
            # 图片名称
            img_alt = img_node_list.get('alt')
            # 正则过滤非法字符
            img_alt = re.sub(r'[\\?<>/|:"*]', '', img_alt)
            # 获取文件后缀名
            img_suffix = os.path.splitext(img_url)[1]
            # 构造图片文件名
            img_name = img_alt + img_suffix
            # 图片保存路径
            img_save_path = './images/'
            if os.path.exists(img_save_path):
                pass
            else:
                os.mkdir(img_save_path)
            img_file_name = img_save_path + img_name
            # 下载图片
            img_downloading = requests.get(img_url)
            with open(img_file_name, 'wb') as f:
                f.write(img_downloading.content)

    def run(self):
        # 遍历
        for pg_num in range(1, self.pageNum+1):
            current_url = self.baseUrl.format(pg_num)
            print('正在解析第%d页' % pg_num)
            self.parse_response(current_url)
            print('第%d页下载成功！' % pg_num)


if __name__ == '__main__':
    expression_downloader = ExpressionDownloader()
    expression_downloader.run()
