# -*- coding: utf-8 -*-
from scrapy import Item, Field


class MainPostItem(Item):
    """ 主题帖对象 """

    # 主题帖所在论坛id
    main_post_forum_id = Field()
    # 主题帖所在论坛名称
    main_post_forum_name = Field()
    # 主题帖id
    main_post_id = Field()
    # 主题帖第一个id
    main_post_first_id = Field()
    # 主题帖话题标志
    main_post_topic_flag = Field()
    # 主题帖置顶标志
    main_post_top_flag = Field()
    # 主题帖精品标志
    main_post_good_flag = Field()
    # 主题帖链接
    main_post_url = Field()
    # 主题帖标题
    main_post_title = Field()
    # 主题帖回复数（回复贴数）
    main_post_reply_count = Field()
    # 主题帖内容
    main_post_content = Field()
    # 主题帖评论数
    main_post_comment_num = Field()
    # 主题帖作者信息
    post_author_infor = Field()


class ReplyPostItem(Item):
    """ 回复贴对象 """

    # 回复贴所在论坛id
    reply_post_forum_id = Field()
    # 回复贴所在论坛名称
    reply_post_forum_name = Field()
    # 回复贴所在主题帖id
    reply_post_main_id = Field()
    # 回复贴所在主题帖名称
    reply_post_main_name = Field()
    # 回复贴id
    reply_post_id = Field()
    # 回复贴内容
    reply_post_content = Field()
    # 回复贴序号
    reply_post_index = Field()
    # 回复贴作者信息
    post_author_infor = Field()
