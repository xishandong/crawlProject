# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YicheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field()
    car_name = scrapy.Field()
    car_num = scrapy.Field()
    car_detail = scrapy.Field()
    car_name1 = scrapy.Field()

