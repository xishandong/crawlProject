# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CaipiaoItem(scrapy.Item):
    qihao = scrapy.Field()
    red_ball = scrapy.Field()
    blue_ball = scrapy.Field()
