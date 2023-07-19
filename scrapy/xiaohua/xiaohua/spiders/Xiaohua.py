import scrapy
from ..items import XiaohuaItem


class XiaohuaSpider(scrapy.Spider):
    name = 'Xiaohua'
    # allowed_domains = ['www.xiaohua.com']
    start_urls = ['https://www.xiaohua.com/duanzi/']

    # 生成一个通用的url模板
    url = 'https://www.xiaohua.com/duanzi?page=%d'
    page_num = 2

    def parse(self, response):
        div_list = response.xpath('/html/body/div/div[8]/div[2]/div[2]/div[@class="one-cont"]')
        all_data = []
        for div in div_list:
            author = div.xpath('./div/div/a/i/text()')[0].extract()
            content = div.xpath('./p/a//text()').extract()
            # 将列表转化为字符串
            content = ''.join(content)
            item = XiaohuaItem()
            item['author'] = author
            item['content'] = content
            # 将item提交给管道
            yield item

            if self.page_num <= 3:
                new_url = format(self.url % self.page_num)
                self.page_num += 1
                # 手动请求发送;callback回调函数是专门用作数据解析
                yield scrapy.Request(url=new_url, callback=self.parse)
