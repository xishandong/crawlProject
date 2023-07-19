# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossjobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pay = scrapy.Field()  # 薪资
    job_name = scrapy.Field()  # 岗位
    detail_url = scrapy.Field()  # 职位详情链接
    company_name = scrapy.Field()  # 公司名称
    requirement = scrapy.Field()  # 要求
    detail = scrapy.Field()
