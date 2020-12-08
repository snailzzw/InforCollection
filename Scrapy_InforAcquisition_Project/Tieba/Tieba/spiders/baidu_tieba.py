# -*- coding: utf-8 -*-
import scrapy
from Tieba.items import MainPostItem, ReplyPostItem
import re
from lxml import etree
import json


class BaiduTiebaSpider(scrapy.Spider):
    name = 'baidu_tieba'
    base_url = 'https://tieba.baidu.com'
    # 帖吧url
    search_url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'
    # 主题帖详情url
    main_post_detail_url = 'https://tieba.baidu.com/p/{}?pn=1'
    # 作者信息url
    author_infor_url = 'https://tieba.baidu.com/home/main?un={}&ie=utf-8&id={}&fr=pb'

    def start_requests(self):
        # 贴吧名称
        start_keywords = ['丁真']
        for keyword in start_keywords:
            global mark
            mark = keyword
            # 构造请求，从第一页开始
            yield scrapy.Request(
                url=self.search_url.format(keyword, 0),
                callback=self.parse_main_post
            )

    def parse_main_post(self, response):
        """
        解析贴吧首页
        获取最后一页的页码，遍历获取贴吧所有帖子
        提取主题帖相关信息，构造帖子详情页url
        """

        # # 如果是第一页，获取最后一页页码
        # if response.url.endswith('pn=0'):
        #     last_page_num = int(re.findall(r'<a href=".*?pn=(.*?)" .*?>尾页</a>', response.text)[0])
        #     # 构造从第二页至最后一页的url列表，步长为50,回调解析
        #     url_list = [self.search_url.format(mark, pg_num) for pg_num in range(50, last_page_num+50, 50)]
        #     for current_url in url_list:
        #         yield scrapy.Request(
        #             url=current_url,
        #             callback=self.parse_main_post
        #         )

        # 解析前进行反爬处理，去注释
        content = response.text
        content = content.replace("<!--", "").replace("-->", "")
        # 帖子列表内容
        post_list_content = etree.HTML(content)

        """解析主题帖列表数据"""

        # 如果是首页，先处理话题
        if response.url.endswith('pn=0'):
            # 今日话题帖列表
            main_posts_topic_list = post_list_content.xpath('//*[@id="threadListGroupCnt"]')
            if len(main_posts_topic_list):
                for main_post_topic_list in main_posts_topic_list:
                    main_post_item = MainPostItem()
                    # 主题帖话题标志为 1
                    main_post_item['main_post_topic_flag'] = 1
                    # 主题帖话题链接
                    main_post_topic_url = main_post_topic_list.xpath('.//a[@class="word_live_title"]/@href')[0]
                    main_post_item['main_post_url'] = 'https:' + main_post_topic_url
                    # 主题帖话题标题
                    main_post_topic_title = main_post_topic_list.xpath('.//a[@class="word_live_title"]/text()')[0]
                    main_post_item['main_post_title'] = "".join(str(main_post_topic_title).split())
                    # 主题帖话题回复数
                    main_post_topic_comment_num = main_post_topic_list.xpath('.//span[@id="interviewReply"]/text()')[0]
                    main_post_item['main_post_reply_count'] = main_post_topic_comment_num
                    # 向话题主题帖详情页发送请求（第一页），主题帖对象为携带参数

            # 非话题贴，有以下几种：1.置顶帖 2.精华帖 3.一般贴
            # 置顶主题帖列表
            main_posts_top_list = post_list_content.xpath('//*[@id="thread_top_list"]//li')
            # 如果存在置顶主题帖
            if len(main_posts_top_list):
                for main_post_top_list in main_posts_top_list:
                    # 主题帖对象
                    main_post_item = MainPostItem()
                    # 1 代表是置顶主题帖，0 代表是非置顶主题帖
                    main_post_item['main_post_top_flag'] = 1
                    # 置顶主题帖相关信息
                    main_post_top_infor = main_post_top_list.get('data-field')
                    main_post_top_infor = json.loads(main_post_top_infor)
                    # 主题帖id
                    main_post_id = main_post_top_infor['id']
                    main_post_item['main_post_id'] = str(main_post_id)
                    # 主题帖firstID
                    main_post_first_id = main_post_top_infor['first_post_id']
                    main_post_item['main_post_first_id'] = str(main_post_first_id)
                    # 判断主题帖是否是精品贴
                    if main_post_top_infor['is_good'] == True:
                        main_post_item['main_post_good_flag'] = 1
                    else:
                        main_post_item['main_post_good_flag'] = 0
                    # 置顶主题帖链接
                    main_post_item['main_post_url'] = self.main_post_detail_url.format(main_post_id)
                    # 置顶主题帖标题
                    main_post_title= main_post_top_list.xpath('.//a[contains(@class,"tit")]/text()')[0]
                    main_post_item['main_post_title'] = main_post_title
                    # 置顶主题帖回复数
                    main_post_comment_num = main_post_top_infor['reply_num']
                    main_post_item['main_post_reply_count'] = main_post_comment_num
                    # 向主题帖详情页发送请求（第一页），主题帖对象为携带参数
                    yield scrapy.Request(
                        url=main_post_item['main_post_url'],
                        meta={'item': main_post_item},
                        callback=self.parse_main_post_detail
                    )

        # 非置顶主题帖（如果不是首页，则无置顶主题帖）
        # 非置顶主题帖列表，过滤掉广告
        main_posts_other_list = post_list_content.xpath('//li[@class=" j_thread_list clearfix"]')
        for main_post_other_list in main_posts_other_list:
            # 主题帖对象
            main_post_item = MainPostItem()
            # 主题帖置顶标志设为0
            main_post_item['main_post_top_flag'] = 0
            # 非置顶主题帖相关信息
            main_post_other_infor = main_post_other_list.get('data-field')
            main_post_other_infor = json.loads(main_post_other_infor)
            # 主题帖id
            main_post_id = main_post_other_infor['id']
            main_post_item['main_post_id'] = str(main_post_id)
            # 主题帖firstID
            main_post_first_id = main_post_other_infor['first_post_id']
            main_post_item['main_post_first_id'] = str(main_post_first_id)
            # 判断是否是精品主题帖
            if main_post_other_infor['is_good'] == True:
                main_post_item['main_post_good_flag'] = 1
            else:
                main_post_item['main_post_good_flag'] = 0
            # 非置顶主题帖链接
            main_post_item['main_post_url'] = self.main_post_detail_url.format(main_post_id)
            # 非置顶主题帖标题
            main_post_title = main_post_other_list.xpath('.//a[contains(@class,"tit")]/text()')[0]
            main_post_item['main_post_title'] = main_post_title
            # 非置顶主题帖回复数
            main_post_comment_num = main_post_other_infor['reply_num']
            main_post_item['main_post_reply_count'] = main_post_comment_num
            # print(main_post_item)
            # 向非置顶主题帖详情页发送请求（第一页），主题帖对象为携带参数
            # yield scrapy.Request(
            #     url=main_post_item['main_post_url'],
            #     meta={'item': main_post_item},
            #     callback=self.parse_main_post_detail
            # )

    def parse_main_post_detail(self, response):
        """
        解析主题帖详情页，解析回复贴和评论帖
        构造作者信息url
        """
        # 如果是首页，获取最后一页页码
        # if response.url.endswith('pn=1'):
        #     # 最后一页页码，注意强转
        #     last_page_num = int(re.findall(r'.*?\?pn=(.*?)">尾页</a>', response.text)[0])
        #     # 主题帖详情页url列表
        #     main_post_detail_url_list = [response.url.replace('pn=1', 'pn={}'.format(pg_num)) for pg_num in range(2, last_page_num+1)]
        #     # 遍历
        #     for current_url in main_post_detail_url_list:
        #         yield scrapy.Request(
        #             url=current_url,
        #             callback=self.parse_main_post_detail
        #         )

        # 解析前进行反爬处理，去注释
        content = response.text
        content = content.replace("<!--", "").replace("-->", "")
        post_detail_content  = etree.HTML(content)

        """
        解析帖子详情数据,只有第一页有主题帖
        第一条帖子为主题帖，其他帖子为回复贴，其余为评论
        """
        if response.url.endswith('pn=1'):
            # 获取主题帖对象
            main_post_item = response.meta['item']
            # 主题帖详细信息
            main_post_detail_list = post_detail_content.xpath('//*[@id="j_p_postlist"]/div[1]')[0]
            main_post_detail_infor = json.loads(main_post_detail_list.get('data-field'))
            # 主题帖详细内容
            main_post_detail_infor_content = main_post_detail_infor['content']
            # 主题帖所在贴吧id
            main_post_item['main_post_forum_id'] = str(main_post_detail_infor_content['forum_id'])
            # 主题帖所在贴吧名称
            main_post_item['main_post_forum_name'] = mark + '吧'
            # 主题帖内容
            main_post_item['main_post_content'] = main_post_detail_infor_content['content']
            main_post_item['main_post_content'] = ''.join(str(main_post_item['main_post_content']).split())
            # 主题帖评论数
            main_post_item['main_post_comment_num'] = main_post_detail_infor_content['comment_num']

            # 主题帖作者信息
            main_post_author_infor = dict()
            # 主题帖作者信息
            main_post_author_infor_content = main_post_detail_infor['author']
            # 主题帖作者id
            main_post_author_user_id = main_post_author_infor_content['user_id']
            main_post_author_infor['post_author_user_id'] = str(main_post_author_user_id)
            # 主题帖作者用户名
            main_post_author_user_name = main_post_author_infor_content['user_name']
            main_post_author_infor['post_author_user_name'] = main_post_author_user_name
            # 主题帖作者昵称
            main_post_author_nickname = main_post_author_infor_content['user_nickname']
            main_post_author_infor['post_author_user_nickname'] = main_post_author_nickname
            # 主题帖作者详情信息链接
            main_post_author_portrait = main_post_author_infor_content['portrait']
            main_post_author_url = self.author_infor_url.format(main_post_author_user_name, main_post_author_portrait)
            main_post_author_infor['post_author_url'] = main_post_author_url
            # 主题帖作者标签
            main_post_author_icons= main_post_detail_list.xpath('.//li[@class="d_icons"]//a/@title')
            main_post_author_infor['post_author_icons'] = main_post_author_icons
            # 主题帖作者认证等级和名称
            main_post_author_level_num = main_post_detail_list.xpath('.//div[@class="p_badge"]//div[2]/text()')[0]
            main_post_author_level_name = main_post_detail_list.xpath('.//div[@class="p_badge"]//div[1]/text()')[0]
            main_post_author_infor['post_author_level_num'] = main_post_author_level_num
            main_post_author_infor['post_author_level_name'] = main_post_author_level_name
            main_post_item['post_author_infor'] = main_post_author_infor
            # 向作者主页发送请求，获取作者详细信息
            yield scrapy.Request(
                url=main_post_author_url,
                meta={'item': main_post_item},
                callback=self.parse_author_infor
            )

        # 回复贴详细内容
        reply_post_detail_list = post_detail_content.xpath('//*[@id="j_p_postlist"]/div[position()>1]')
        for reply_post_detail in reply_post_detail_list:
            # 回复贴对象
            reply_post_item = ReplyPostItem()
            # 回复贴内容
            reply_post_content_infor = json.loads(reply_post_detail.get('data-field'))
            reply_post_content = reply_post_content_infor['content']
            # 回复贴所在论坛id
            reply_post_item['reply_post_forum_id'] = str(reply_post_content['forum_id'])
            # 回复贴所在论坛名称
            reply_post_item['reply_post_forum_name'] = mark + '吧'
            # 回复贴所在主题帖id
            reply_post_item['reply_post_main_id'] = str(reply_post_content['thread_id'])
            # 回复贴id
            reply_post_item['reply_post_id'] = str(reply_post_content['post_id'])
            # 回复贴内容
            reply_post_item['reply_post_content'] = reply_post_content['content']
            # 在本贴中第几个发言（从1开始）
            reply_post_item['reply_post_index'] = reply_post_content['post_index']

            # 回复贴作者信息
            reply_post_author = reply_post_content_infor['author']
            # 如果有广告，将其过滤
            if "portrait" and "user_nickname" in reply_post_author:
                # 回复贴作者信息
                reply_post_author_infor = dict()

                # 回复贴作者id
                reply_post_author_user_id = reply_post_author['user_id']
                reply_post_author_infor['post_author_user_id'] = str(reply_post_author_user_id)
                # 回复贴作者用户名
                reply_post_author_user_name = reply_post_author['user_name']
                reply_post_author_infor['post_author_user_name'] = reply_post_author_user_name
                # 回复贴作者昵称
                reply_post_author_nickname = reply_post_author['user_nickname']
                reply_post_author_infor['post_author_user_nickname'] = reply_post_author_nickname
                # print(reply_post_author_infor)
                # # 回复贴作者详情信息链接
                reply_post_author_portrait = reply_post_author['portrait']
                reply_post_author_url = self.author_infor_url.format(reply_post_author_user_name, reply_post_author_portrait)
                reply_post_author_infor['post_author_url'] = reply_post_author_url
                # 回复贴作者标签
                reply_post_author_icons = reply_post_detail.xpath('.//li[@class="d_icons"]//a/@title')
                reply_post_author_infor['post_author_icons'] = reply_post_author_icons
                # 回复贴作者认证等级和名称
                reply_post_author_level_num = reply_post_detail.xpath('.//div[@class="p_badge"]//div[2]/text()')[0]
                main_post_author_level_name = reply_post_detail.xpath('.//div[@class="p_badge"]//div[1]/text()')[0]
                reply_post_author_infor['post_author_level_num'] = reply_post_author_level_num
                reply_post_author_infor['post_author_level_name'] = main_post_author_level_name
                reply_post_item['post_author_infor'] = reply_post_author_infor
                # 向作者主页发送请求，获取作者详细信息
                yield scrapy.Request(
                    url=reply_post_author_url,
                    meta={'item': reply_post_item},
                    callback=self.parse_author_infor
                )
            else:
                pass

    def parse_author_infor(self, response):
        """解析作者信息"""

        # 接收参数
        item = response.meta['item']
        author_infor = item['post_author_infor']
        # 解析前进行反爬处理，去注释
        content = response.text
        content = content.replace("<!--", "").replace("-->", "")
        post_author_content  = etree.HTML(content)

        # 作者头像
        post_author_img = post_author_content.xpath('//*[@id="userinfo_wrap"]//img/@src')[0]
        author_infor['post_author_img'] = post_author_img

        # 作者性别
        post_author_sex = post_author_content.xpath('//*[@id="userinfo_wrap"]//span[contains(@class,"sex")]/@class')[0]
        if post_author_sex  == 'userinfo_sex userinfo_sex_male':
            author_infor['post_author_gender'] = '男'
        elif post_author_sex  == 'userinfo_sex userinfo_sex_female':
            author_infor['post_author_gender'] = '女'
        else:
            author_infor['post_author_gender'] = ''
        # 吧龄
        post_author_age = post_author_content.xpath('//*[@id="userinfo_wrap"]//span[contains(text(),"吧龄")]/text()')[0]
        post_author_age = str(post_author_age).replace('吧龄:', '')
        author_infor['post_author_age'] = post_author_age
        # 发帖
        post_author_post_num = post_author_content.xpath('//*[@id="userinfo_wrap"]//span[contains(text(),"发贴")]/text()')[0]
        post_author_post_num = str(post_author_post_num).replace('发贴:', '')
        author_infor['post_author_post_num'] = post_author_post_num
        # 礼物数
        post_author_gift_num = post_author_content.xpath('//span[@class="gift-num"]/i/text()')[0]
        author_infor['post_author_gift_num'] = post_author_gift_num
        # 关注人数
        post_author_concern_count = post_author_content.xpath('//span[@class="concern_num"]/a[contains(@href,"concern")]/text()')
        if len(post_author_concern_count):
            author_infor['post_author_concern_count'] = post_author_concern_count[0]
        # 关注作者的人
        post_author_fan_count = post_author_content.xpath('//span[@class="concern_num"]/a[contains(@href,"fans")]/text()')
        if len(post_author_fan_count):
            author_infor['post_author_fan_count'] = post_author_fan_count[0]
        item['post_author_infor'] = author_infor
        yield item