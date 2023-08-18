import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from ..items import SunproItem


class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://wz.sun0769.com/political/index/politicsNewest']

    # 实例化一个浏览器对象
    def __init__(self, **kwargs):
        # 实现让selenium规避被检测到的风险
        super().__init__(**kwargs)
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--window-size=1920,1080")  # 建议设置窗口大小
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        option.add_argument('blink-settings=imagesEnabled=false')
        self.bro = webdriver.Chrome(executable_path='D:\爬虫\selenium\chromedriver.exe', options=option)

    def closed(self, spider):
        self.bro.quit()

    # 链接提取器: 根据指定规则(allow=r'正则表达式')进行指定链接提取
    link = LinkExtractor(allow=r'id=1&page=\d', restrict_xpaths='/html/body/div[2]/div[3]/div[3]/div/a')
    # link_detail = LinkExtractor(restrict_xpaths='/html/body/div[2]/div[3]/ul[2]/li/span[3]/a')

    rules = (
        # 规则解析器: 将链接提取器提取到的链接进行指定规则(callback)的解析操作
        # follow=True: 可以将链接提取器继续作用到链接提取器提取到的链接所对应的页面中
        Rule(link, callback='parse_item', follow=True),
        # Rule(link_detail, callback='parse_detail'),
    )

    # 解析投诉的编号和标题
    def parse_item(self, response):
        li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:
            item = SunproItem()
            number = li.xpath('./span[1]/text()').extract_first()
            item['number'] = number
            status = li.xpath('./span[2]/text()').extract_first().strip()
            item['status'] = status
            title = li.xpath('./span[3]/a/text()').extract_first()
            item['title'] = title
            detail_url = 'https://wz.sun0769.com' + li.xpath('./span[3]/a/@href').extract_first()

            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

    # 解析投诉的内容
    def parse_detail(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre//text()').extract()
        content = ''.join(content)
        item['content'] = content
        city = response.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/span[2]/text()').extract_first()
        c = re.sub(' 来自：', '', city)
        C = re.sub(' ', '', c)
        item['city'] = C
        time = response.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/span[3]/text()').extract_first()
        item['time'] = time
        # print(item)
        yield item
