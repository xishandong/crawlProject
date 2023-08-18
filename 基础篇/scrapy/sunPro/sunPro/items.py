# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SunproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    number = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    content = scrapy.Field()
    city = scrapy.Field()
    time = scrapy.Field()

# class DetailItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     id = scrapy.Field()
#     content = scrapy.Field()