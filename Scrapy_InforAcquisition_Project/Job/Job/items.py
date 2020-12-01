# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentJobItem(scrapy.Item):
    """腾讯招聘岗位数据建模"""

    # 岗位id
    job_post_id = scrapy.Field()
    # 岗位名称
    job_name = scrapy.Field()
    # 岗位所在国家
    job_country_name = scrapy.Field()
    # 岗位所在地点
    job_location_name = scrapy.Field()
    # 岗位所在小组
    job_group = scrapy.Field()
    # 岗位所在小组id（BGID）
    job_group_id = scrapy.Field()
    # 岗位负责产品
    job_product_name = scrapy.Field()
    # 岗位类别
    job_category_name = scrapy.Field()
    # 岗位需求
    job_requirement = scrapy.Field()
    # 岗位职责
    job_responsibility = scrapy.Field()
    # 岗位更新时间
    job_updated_time = scrapy.Field()
