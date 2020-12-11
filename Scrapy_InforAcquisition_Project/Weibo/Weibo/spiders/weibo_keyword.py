# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
import time
from Weibo.items import TweetsItem, CommentsItem
from Weibo.spiders.utils import time_fix
from scrapy.selector import Selector


class WeiboKeywordSpider(scrapy.Spider):
    name = 'weibo_keyword'
    base_url = 'https://weibo.cn'

    def start_requests(self):
        start_keywords = ['香港']
        for keyword in start_keywords:
            global mark
            mark = keyword
            # 发送请求
            yield scrapy.Request(
                url='https://weibo.cn/search/mblog?keyword={}&sort=hot&page=1'.format(keyword),
                callback=self.parse_tweet
            )

    def parse_tweet(self, response):
        """解析微博"""

        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield scrapy.Request(page_url, self.parse_tweet, dont_filter=True, meta=response.meta)

        """解析本页数据"""
        tree_content = etree.HTML(response.body)
        # 获取本页所有内容
        tweet_nodes = tree_content.xpath('//div[@class="c" and @id]')

        for tweet_node in tweet_nodes:
            tweet_item = TweetsItem()
            # 微博抓取时间戳
            tweet_item['tweet_crawled_at'] = int(time.time())

            tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
            user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
            # 微博url
            tweet_item['tweet_url'] = 'https://weibo.com/{}/{}'.format(user_tweet_id.group(2),
                                                                    user_tweet_id.group(1))
            # 微博用户id
            tweet_item['user_id'] = user_tweet_id.group(2)
            # 微博id
            tweet_item['tweet_id'] = '{}_{}'.format(user_tweet_id.group(2), user_tweet_id.group(1))
            create_time_info = tweet_node.xpath('//div/span[@class="ct" and contains(text(),"来自")]/text()')[0]
            # 微博发表时间
            tweet_item['tweet_created_at'] = time_fix(create_time_info.split('来自')[0].strip())

            # 微博点赞数
            like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[0]
            tweet_item['tweet_attitude_count'] = int(re.search('\d+', like_num).group())

            # 微博转发数
            repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[0]
            tweet_item['tweet_repost_count'] = int(re.search('\d+', repost_num).group())

            # 微博评论数
            comment_num = tweet_node.xpath('.//a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[0]
            tweet_item['tweet_comment_count'] = int(re.search('\d+', comment_num).group())

            # 微博标记
            tweet_item['tweet_mark'] = mark

            # 微博来源
            tweet_source = tweet_node.xpath('//div/span[@class="ct" and contains(text(),"来自")]/text()')[0]
            tweet_item['tweet_source'] = re.findall(".*来自(.*)", str(tweet_source).replace(u"\xa0", ""))[0]

            # 微博内容
            tweet_content_node = tweet_node.xpath('.//span[@class="ctt"]')
            if tweet_content_node:
                all_content = tweet_content_node[0].xpath('string(.)').strip('\u200b')
                all_content = re.findall(":(.*)", all_content)
                if all_content:
                    tweet_item['tweet_content'] = all_content[0]

            # 抓取该微博的评论信息
            comment_url = self.base_url + '/comment/' + tweet_item['tweet_url'].split('/')[-1] + '?page=1'

            yield scrapy.Request(
                url=comment_url,
                callback=self.parse_comment,
                meta={'tweet_url': tweet_item['tweet_url']},
                priority=1)

            # 请求用户首页，抓取微博用户信息
            yield scrapy.Request(
                url="https://weibo.cn/u/%s" % user_tweet_id.group(2),
                callback=self.parse_user_page,
                meta={'item': tweet_item},
                priority=1)

            # 请求用户资料页，抓取微博用户资料
            user_infor_url = "https://weibo.cn/%s/info" % user_tweet_id.group(2)
            yield scrapy.Request(
                url=user_infor_url,
                callback=self.parse_user_infor,
                meta={'item': tweet_item},
                priority=1)


    def parse_comment(self, response):
        """解析微博评论信息"""

        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield scrapy.Request(page_url, self.parse_comment, dont_filter=True, meta=response.meta)

        selector = Selector(response)
        comment_nodes = selector.xpath('//div[@class="c" and contains(@id,"C_")]')
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href').extract_first()
            if not comment_user_url:
                continue
            # 评论对象实例化
            comment_item = CommentsItem()
            # 评论采集时间
            comment_item['comment_crawled_at'] = int(time.time())
            # 评论微博url
            comment_item['comment_tweet_url'] = response.meta['tweet_url']
            uid = re.search(r'/u/(\d+)', comment_user_url).group(1)
            # 评论用户id
            comment_item['user_id'] = uid
            # 评论内容
            comment_item['comment_content'] = comment_node.xpath('.//span[@class="ctt"]').xpath('string(.)').extract_first()
            # 评论id
            comment_item['comment_id'] = comment_node.xpath('./@id').extract_first()
            created_at = comment_node.xpath('.//span[@class="ct"]/text()').extract_first()
            # 评论发表时间
            comment_item['comment_created_at'] = time_fix(created_at.split('\xa0')[0])
            # 评论标志
            comment_item['comment_mark'] = mark

            # 请求用户首页，抓取评论用户信息
            yield scrapy.Request(
                url="https://weibo.cn/u/%s" % uid,
                callback=self.parse_user_page,
                meta={'item': comment_item},
                priority=1)

            # 请求用户资料页，抓取评论用户资料
            user_infor_url = "https://weibo.cn/%s/info" % uid
            yield scrapy.Request(
                user_infor_url,
                callback=self.parse_user_infor,
                meta={'item': comment_item},
                priority=1)

    def parse_user_page(self, response):
        """获取用户简要信息"""

        item = response.meta['item']
        text = response.text
        tweets_num = re.findall('微博\[(\d+)\]', text)
        if tweets_num:
            item['user_tweets_num'] = tweets_num[0]
        follows_num = re.findall('关注\[(\d+)\]', text)
        if follows_num:
            item['user_follows_num'] = follows_num[0]
        fans_num = re.findall('粉丝\[(\d+)\]', text)
        if fans_num:
            item['user_fans_num'] = fans_num[0]
        groups_num = re.findall('分组\[(\d+)\]', text)
        if fans_num:
            item['user_groups_num'] = groups_num[0]
        yield item

    def parse_user_infor(self, response):
        """ 抓取微博用户个人资料信息 """

        item = response.meta['item']
        # 用户采集时间
        item['user_crawled_at'] = int(time.time())
        selector = Selector(response)
        # 获取标签里的所有text()
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())
        nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        briefIntroduction = re.findall('简介;[：:]?(.*?);', text1)
        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
        sentiment = re.findall('感情状况;?[：:]?(.*?);', text1)
        vip_level = re.findall('会员等级;?[：:]?(.*?);', text1)
        authentication = re.findall('认证;?[：:]?(.*?);', text1)

        img = selector.xpath('//div[@class="c"]/img/@src').extract()
        item['user_img'] = img[0]
        if nick_name and nick_name[0]:
            item['user_nickname'] = nick_name[0].replace(u"\xa0", "")
        if gender and gender[0]:
            item['user_gender'] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            item['user_location'] = place[0]
        if briefIntroduction and briefIntroduction[0]:
            item['user_profile'] = briefIntroduction[0].replace(u"\xa0", "")
        if birthday and birthday[0]:
            item['user_birthday'] = birthday[0]
        if sex_orientation and sex_orientation[0]:
            item['user_sex_orientation'] = sex_orientation[0]
        if sentiment and sentiment[0]:
            item["user_sentiment"] = sentiment[0].replace(u"\xa0", "")
        if vip_level and vip_level[0]:
            item["user_vip_level"] = vip_level[0].replace(u"\xa0", "")
        if authentication and authentication[0]:
            item["user_authentication"] = authentication[0].replace(u"\xa0", "")

        # 判断是否有标签
        label_judge = re.findall('更多', text1)

        if label_judge:
            label_url = 'https://weibo.cn/account/privacy/tags/?uid=' + item['user_id']
            yield scrapy.Request(
                label_url,
                callback=self.parse_user_label,
                meta={'item': item},
                priority=1)
        else:
            yield item

    def parse_user_label(self, response):
        tree_node = etree.HTML(response.body)
        item = response.meta['item']
        tag= tree_node.xpath('//div[@class="c"]//a[contains(@href,"stag")]//text()')
        item['user_tag'] = tag
        yield item



