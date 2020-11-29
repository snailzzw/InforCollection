"""百科高校信息抽取器"""

from InforCollection.headers.UserAgents import get_headers
import requests
from bs4 import BeautifulSoup
import os


class SchoolInforExtractor:
    def __init__(self):
        self.headers = {'User-Agent': get_headers()}
        self.baseUrl = 'https://baike.baidu.com/item/{}'
        self.num = 1

    @staticmethod
    def read_schoolname(filename):
        """读取学校"""
        with open(filename, 'r') as f:
            school_names = f.readlines()
        # 将学校名称保存为列表
        school_name_list = [i.strip() for i in school_names]
        return school_name_list

    @staticmethod
    def school_page_save(data, name):
        """学校信息页面下载"""
        page_save_path = './schoolPages/'
        if os.path.exists(page_save_path):
            pass
        else:
            os.mkdir(page_save_path)
        filename = page_save_path + name + '.html'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)

    def get_response(self, url):
        return requests.get(url, headers=self.headers).content

    def parse_response(self, url, name):
        content = self.get_response(url)
        # 使用bs4库解析页面
        soup = BeautifulSoup(content, 'lxml')
        # 学校页面下载
        self.school_page_save(soup.prettify(), name)
        # 词条属性
        item_attributes = soup.find_all(attrs={'class': 'basicInfo-item name'})
        # 词条属性内容
        item_values = soup.find_all(attrs={'class': 'basicInfo-item value'})
        item_attribute_modify = list()
        item_value_modify = list()
        # 数据清洗(去空格、特定字符)并将修改数据存入列表
        for item_attribute in item_attributes:
            item_attribute_modify.append(item_attribute.text.replace(u'\xa0', ''))
        for item_value in item_values:
            item_value_modify.append(item_value.text.replace('\n', '').replace('收起', ''))
        # 使用dict与zip将学校词条打包成字典(映射为 属性：属性值）
        school_infor_dict = dict(zip(item_attribute_modify, item_value_modify))
        print(name + ' 词条解析成功')
        return school_infor_dict

    @staticmethod
    def school_infor_save(filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(data))
        print("学校信息保存成功")

    def run(self):
        school_infor_list = []
        # 获取学校名字
        school_name_list = self.read_schoolname('./school_name.txt')
        print('共%s条信息' % len(school_name_list))
        # 遍历
        for school_name in school_name_list:
            current_url = self.baseUrl.format(school_name)
            print('id : ' + str(self.num) + ' 正在解析 ' + school_name + ' 词条')
            school_infor = self.parse_response(current_url, school_name)
            school_infor_list.append(school_infor)
            self.num += 1
        self.school_infor_save('./schoolInfor.txt', school_infor_list)


if __name__ == '__main__':
    school_infor = SchoolInforExtractor()
    school_infor.run()
