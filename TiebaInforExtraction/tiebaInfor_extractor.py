"""贴吧信息采集"""

from InforCollection.headers.UserAgents import get_headers
import requests
import re
from lxml import etree
import json


class TiebaInforExtractor:
    """贴吧信息采集"""

    def __init__(self):
        """初始化参数设置"""
        self.headers = {'User-Agent': get_headers()}
        self.keyWord = input('请输入关键字：')
        self.baseUrl = 'https://tieba.baidu.com/f'
        self.firstUrl = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn=0'.format(self.keyWord)
        self.page_num = 1
        self.pn = 0

    def get_content(self, url, params=None):
        """发送请求，返回响应内容"""
        page_req = requests.get(url, params=params, headers=self.headers)
        return page_req.content.decode('utf-8')

    # 静态方法
    @staticmethod
    def parse_content(content):
        """解析网页，抽取信息"""
        # 反爬处理，去掉注释! ! !
        content = content.replace("<!--", "").replace("-->", "")
        page_data = etree.HTML(content)
        articles_infor = page_data.xpath('//li[@class=" j_thread_list clearfix"]')
        all_infor_list = []
        for article_infor in articles_infor:
            all_infor = {}
            # 文章标题
            article_title = article_infor.xpath('.//a[@class="j_th_tit "]//text()')[0]
            # 文章链接
            href = article_infor.xpath('.//a[@class="j_th_tit "]//@href')[0]
            article_href = 'https://tieba.baidu.com/' + href
            all_infor["article_title"] = article_title
            all_infor["article_href"] = article_href
            # 文章作者信息
            author_infor = article_infor.get('data-field')
            author_infor = json.loads(author_infor)
            all_infor["author_infor"] = author_infor
            all_infor_list.append(all_infor)
        return all_infor_list

    def run(self):
        """任务执行"""
        # 获取最后一页的页码
        first_page = requests.get(self.firstUrl).content.decode('utf-8')
        last_page_num = int(re.findall(r'<a href=".*?pn=(.*?)" .*?>尾页</a>', first_page)[0])
        # 第一页到最后一页遍历，步长为50
        print('-------数据开始采集-------共%d页' % (last_page_num//50+1))
        for pg_num in range(self.pn, last_page_num, 50):
            page_content = self.get_content(url=self.baseUrl, params={'kw': self.keyWord, 'ie': 'utf-8', 'pn': pg_num})
            page_infor_list = self.parse_content(page_content)
            print('-------第%d页信息提取完成-------共%d条-------' % (self.page_num, len(page_infor_list)))
            self.page_num += 1
            print(page_infor_list)


if __name__ == '__main__':
    tieba_spider = TiebaInforExtractor()
    tieba_spider.run()
