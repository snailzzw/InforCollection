# -*- coding: utf-8 -*-
import scrapy
from Job.items import TencentJobItem
import json
import math


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    # 基础url
    base_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?' \
               'timestamp=1606801692766&countryId=&cityId=&' \
               'bgIds=&productId=&categoryId=&' \
               'parentCategoryId=&attrId=&keyword=&' \
               'pageIndex={}&pageSize=10&' \
               'language=zh-cn&area=cn'

    def start_requests(self):
        first_pg = 1
        # 初始url(第一页)
        yield scrapy.Request(
            url=self.base_url.format(first_pg), callback=self.parse_response
        )

    def parse_response(self, response):
        # 使用json解析
        json_content = json.loads(response.text)
        # 读取职位数量，并计算页数（向上取整）
        page_num = math.ceil(json_content['Data']['Count']/10)
        # url队列
        url_list = [self.base_url.format(pg_num) for pg_num in range(1, page_num+1)]
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_response)

        """解析数据"""
        job_nodes_list = json_content['Data']['Posts']
        # 职位模型
        job_item = TencentJobItem()

        for job_node_list in job_nodes_list:

            # 岗位id
            job_item['job_post_id'] = job_node_list['RecruitPostId']
            # 岗位名称
            job_item['job_name'] = job_node_list['RecruitPostName']
            # 岗位所在国家
            job_item['job_country_name'] = job_node_list['CountryName']
            # 岗位所在地点
            job_item['job_location_name'] = job_node_list['LocationName']
            # 岗位所在小组
            job_item['job_group'] = job_node_list['BGName']
            # 岗位负责产品
            job_item['job_product_name'] = job_node_list['ProductName']
            # 岗位类别
            job_item['job_category_name'] = job_node_list['CategoryName']
            # 岗位更新时间
            job_item['job_updated_time'] = job_node_list['LastUpdateTime']
            post_id = job_node_list['PostId']
            # 工作详情页url
            post_detail_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?' \
                              'timestamp=1606804081920&postId={}&language=zh-cn'.format(post_id)
            # 获取岗位详细信息
            yield scrapy.Request(
                url=post_detail_url,
                callback=self.parse_detail,
                meta={'item': job_item},
                priority=1
            )

    @staticmethod
    def parse_detail(response):
        """工作详情页解析"""
        # 获取工作对象
        job_item = response.meta['item']
        job_detail_content = json.loads(response.text)

        # 岗位所在小组id
        job_item['job_group_id'] = job_detail_content['Data']['BGId']
        # 岗位需求
        job_item['job_requirement'] = job_detail_content['Data']['Requirement']
        job_item['job_requirement'] = " ".join(str(job_item['job_requirement']).split())
        # 岗位职责
        job_item['job_responsibility'] = job_detail_content['Data']['Responsibility']
        job_item['job_responsibility'] = " ".join(str(job_item['job_responsibility']).split())
        # 返回数据对象
        yield job_item
