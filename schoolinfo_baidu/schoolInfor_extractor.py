#高校信息抽取器

from InforCollection.headers.UserAgents import get_headers
import requests
from bs4 import BeautifulSoup
import os



#读取学校名称文件
def schoolName_read(filename):
    with open(filename,'r') as f:
        all_schoolName = f.readlines()
    #将学校名称保存为列表
    schoolName = [i.strip() for i in all_schoolName]
    return schoolName

#将学校信息页面保存为html文件
def schoolPage_save(data,name):
    page_save_path = './schoolPages/'
    if os.path.exists(page_save_path):
        pass
    else:
        os.mkdir(page_save_path)
    filename = page_save_path + name + '.html'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

#学校信息保存到txt文件中
def schoolInfo_sava(filename,data):
    with open(filename,'w',encoding='utf-8') as f:
        f.write(str(data))
    print("学校信息保存成功")

#解析页面
def parse_page(url,name,all_schoolInfor):
    headers = {'User-Agent':get_headers()}
    response = requests.get(url,headers=headers)
    #使用bs4库解析页面
    soup = BeautifulSoup(response.content,'lxml')
    #下载网页
    schoolPage_save(soup.prettify(),name)
    print(name + " 页面下载成功")
    #词条属性
    item_attributes = soup.find_all(attrs={'class':'basicInfo-item name'})
    #词条属性内容
    item_values = soup.find_all(attrs={'class':'basicInfo-item value'})

    item_attributeModify = []
    item_valueModify = []

    # 数据清洗(去空格、特定字符)并将修改数据存入列表
    for item_attribute in item_attributes:
        item_attributeModify.append(item_attribute.text.replace(u'\xa0',''))
    for item_value in item_values:
        item_valueModify.append(item_value.text.replace('\n','').replace('收起',''))

    #使用dict与zip将学校词条打包成字典(映射为 属性：属性值）
    schoolInfor = dict(zip(item_attributeModify,item_valueModify))
    #将学校信息加入队列
    all_schoolInfor.append(schoolInfor)
    print(name + ' 词条添加成功')


def main():
    all_schoolInfor = []
    schoolName = schoolName_read('./school_name.txt')
    print('共%d条信息' % len(schoolName))
    num = 1
    for name in schoolName:
        school_url = 'https://baike.baidu.com/item/{}'.format(name)
        print('id : ' + str(num) + ' 正在解析 ' + name + ' 词条')
        parse_page(school_url,name,all_schoolInfor)
        num += 1
    schoolInfo_sava('./schoolInfor.txt',all_schoolInfor)
    print('词条信息保存成功')

if __name__ == '__main__':
    main()
