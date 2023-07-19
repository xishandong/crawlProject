import scrapy
from ..items import CaipiaoItem
from selenium import webdriver
from selenium.webdriver import ChromeOptions

class SeqSpider(scrapy.Spider):
    name = 'seq'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://datachart.500.com/ssq/']

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
        # option.add_argument('blink-settings=imagesEnabled=false')
        self.bro = webdriver.Chrome(executable_path='D:\爬虫\selenium\chromedriver.exe', options=option)

    def closed(self, spider):
        self.bro.quit()

    def parse(self, response):
        tr_list = response.xpath('//*[@id="tdata"]/tr')
        for tr in tr_list:
            item = CaipiaoItem()
            # 过滤掉没用的标签
            if tr.xpath('./@class').extract_first() == 'tdbck':
                continue
            qishu = tr.xpath('./td[1]/text()').extract_first().strip()
            # 也可以用xpath: red_ball = tr.xpath("./td[@class="chartBall01"]/text()").extract()
            red_ball = tr.css(".chartBall01::text").extract()
            blue_ball = tr.css(".chartBall02::text").extract_first()
            item['qihao'] = qishu
            item['red_ball'] = red_ball
            item['blue_ball'] = blue_ball

            yield item
