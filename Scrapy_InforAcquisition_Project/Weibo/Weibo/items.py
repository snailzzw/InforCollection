# -*- coding: utf-8 -*-

from scrapy import Item, Field


class UserItem(Item):
    """微博用户模型"""

    # 用户ID
    user_id = Field()
    # 用户昵称
    user_nickname = Field()
    # 用户性别
    user_gender = Field()
    # 用户所在地区
    user_location = Field()
    # 用户简介
    user_profile = Field()
    # 用户生日
    user_birthday = Field()
    # 用户微博数
    user_tweets_num = Field()
    # 用户关注数
    user_follows_num = Field()
    # 用户粉丝数
    user_fans_num = Field()
    # 用户分组数
    user_groups_num = Field()
    # 用户标签
    user_tag = Field()
    # 用户头像
    user_img = Field()
    # 用户性取向
    user_sex_orientation = Field()
    # 用户感情状况
    user_sentiment = Field()
    # 用户会员等级
    user_vip_level = Field()
    # 用户认证
    user_authentication = Field()
    # 用户首页
    user_infor_url = Field()
    # 抓取时间戳
    user_crawled_at = Field()


class TweetsItem(UserItem):
    """微博模型"""

    # 微博id
    tweet_id = Field()
    # 微博url
    tweet_url = Field()
    # 微博发表时间
    tweet_created_at = Field()
    # 微博内容
    tweet_content = Field()
    # 微博转发内容
    repost_content = Field()
    # 微博点赞数
    tweet_attitude_count = Field()
    # 微博转发数
    tweet_repost_count = Field()
    # 微博评论数
    tweet_comment_count = Field()
    # 微博来源
    tweet_source = Field()
    # 微博采集时间戳
    tweet_crawled_at = Field()
    # 微博采集任务标记
    tweet_mark = Field()


class CommentsItem(UserItem):
    """微博评论模型"""

    # 微博评论id
    comment_id = Field()
    # 微博评论创建时间
    comment_created_at = Field()
    # 微博评论内容
    comment_content = Field()
    # 微博评论所属微博url
    comment_tweet_url = Field()
    # 微博评论点赞数
    comment_attitude_count = Field()
    # 微博评论采集时间戳
    comment_crawled_at = Field()
    # 微博评论任务标记
    comment_mark = Field()