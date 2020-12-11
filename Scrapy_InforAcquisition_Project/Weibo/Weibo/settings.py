# -*- coding: utf-8 -*-

BOT_NAME = 'Weibo'

SPIDER_MODULES = ['Weibo.spiders']
NEWSPIDER_MODULE = 'Weibo.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.2


# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Weibo.middlewares.WeiboSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Weibo.middlewares.WeiboDownloaderMiddleware': 543,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
   'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
   'Weibo.middlewares.CookieMiddleware': 300,
   'Weibo.middlewares.RedirectMiddleware': 200,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Weibo.pipelines.MongoDBPipline': 300,
}

LOCAL_MONGO_HOST = 'localhost'

LOCAL_MONGO_PORT = 27017
# 存放数据的数据库
Data_DB_NAME = 'weibo'
# 账户数据库
Account_DB_NAME = 'account'

USER = 'root'
PWD = 'mongo'