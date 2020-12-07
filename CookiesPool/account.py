"""Cookie池搭建"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import time
import pymongo


class CookieBuild:


    def __init__(self):
        """初始化"""
        # 账号队列
        self.account_list = list()
        # selenium初始化配置
        self.firefox_options = Options()
        self.client = pymongo.MongoClient(host='localhost', port=27017, username='root', password='mongo')['account']
        # # 添加User-Agent
        # self.firefox_options.add_argument('user-agent='+self.headers)
        # # 隐身模式
        # self.firefox_options.add_argument("--incognito")

    def set(self, account, sep='----'):
        """账号格式化"""
        username, password = account.split(sep)
        # 账号转换元组
        self.account_list.append((username, password))

    def scan(self):
        """账号录入"""
        print('请输入账号密码组, 输入exit退出读入')
        while True:
            account = input()
            if account == 'exit':
                break
            # 格式化账号
            self.set(account)

    def account_build(self, account_list):
        """Cookies获取"""
        for account in account_list:
            account_infor = dict()
            # 登录账号
            account_user = account[0]
            # 登录密码
            account_pwd = account[1]
            account_infor['username'] = account_user
            account_infor['password'] = account_pwd
            # Chrome对象
            global driver
            self.driver = webdriver.Firefox(options=self.firefox_options)
            # 隐式等待
            self.driver.implicitly_wait(3)
            # 打开通行证登录页面
            self.driver.get('https://login.sina.com.cn/signup/signin.php')
            # 用户名输入
            self.driver.find_element_by_id('username').send_keys(account_user)
            # 密码输入
            self.driver.find_element_by_id('password').send_keys(account_pwd)
            # 取消自动登录
            self.driver.find_element_by_id('remLoginName').click()
            # 点击登录按钮
            self.driver.find_element_by_xpath('//*[@id="vForm"]//input[@value="登 录"]').click()
            text = self.driver.find_elements_by_xpath('//*[@id="login_err"]/span/i[2]')
            if len(text) and text[0].text == "登录名或密码错误":
                print('-' * 7 + '账号密码错误，请重新输入' + '-' * 7)
                # 关闭浏览器页面
                self.driver.close()
            else:
                self.get_cookie(account_infor)

    def get_cookie(self, account_infor):

        # 切换窗口句柄
        self.driver.switch_to.window(self.driver.window_handles[0])
        print(self.driver.current_url)
        # 页面跳转判断
        condition = expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, "logo")
        )
        try:
            WebDriverWait(self.driver, 20, 0.5).until(
                condition
            )
            print('-' * 7 + '账号登录成功,页面跳转' + '-' * 7)
            self.driver.get('https://weibo.cn/')
            # 获取并格式化Cookie
            cookie = ''
            for data in self.driver.get_cookies():
                cookie += data['name'] + '=' + data['value'] + ';'
            account_infor['Cookie'] = cookie
            self.insert_account(account_infor)
            self.driver.quit()
        except Exception as e:
            print('-'*7 + '账号登录失败' + '-'*7)
            print(e)
            self.driver.close()

    def insert_account(self, account_infor):
        """账号入库"""
        self.client['weibo'].insert_one(account_infor)
        print(account_infor['username']+'入库成功！')

    def run(self):
        # 账号录入并格式化
        self.scan()
        print(len(set(self.account_list)))
        # 账号去重并进行登录
        # self.account_build(set(self.account_list))


if __name__ == '__main__':
    cookie_build = CookieBuild()
    cookie_build.run()
