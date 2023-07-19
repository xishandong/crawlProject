import scrapy
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from ..items import WangyiItem


class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    models_url = []  # 存放板块的详情页url
    number = 1

    # 实例化一个浏览器对象
    def __init__(self, **kwargs):
        # 实现让selenium规避被检测到的风险
        super().__init__(**kwargs)
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--window-size=1920,1080")  # 建议设置窗口大小
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        self.bro = webdriver.Chrome(executable_path='D:\爬虫\selenium\chromedriver.exe', options=option)

    def closed(self, spider):
        self.bro.quit()

    # 解析每一个板块对应的详情页url
    # 每一个板块对应新闻相关的内容都是动态加载出来的
    def detail_parse(self, response):
        div_list = response.xpath('//div[@class="ndi_main"]/div[@class="data_row news_article clearfix news_first"] | //div[@class="ndi_main"]/div[@class="data_row news_article clearfix "]')
        # print(div_list)
        for div in div_list:
            item = WangyiItem()
            title = div.xpath('./div/div/h3/a/text()').extract_first()
            item['title'] = title
            item['number'] = self.number
            self.number += 1
            content_url = div.xpath('./div/div/h3/a/@href').extract_first()

            yield scrapy.Request(url=content_url, callback=self.content_parse, meta={'item': item})

    # 解析新闻内容
    def content_parse(self, response):
        item = response.meta['item']
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        content = ''.join(content)
        item['content'] = content
        # print(item)
        yield item

    # 解析五大板块的详情页url
    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[3]/div[2]/div[2]/div[2]/div/ul/li')
        alist = [1, 2, 4, 5]  # 存储各个领域的li标签编号

        for index in alist:
            model_url = li_list[index].xpath('./a/@href').extract_first()
            # print(model_url)
            self.models_url.append(model_url)

        # 依次对每个板块进行发起请求
        for url in self.models_url:
            yield scrapy.Request(url=url, callback=self.detail_parse)
