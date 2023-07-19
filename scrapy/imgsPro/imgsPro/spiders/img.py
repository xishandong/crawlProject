import scrapy
from ..items import ImgsproItem
import re


class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://sc.chinaz.com/tupian//']
    page_num = 2

    def parse(self, response):

        div_list = response.xpath('/html/body/div[3]/div[2]/div')
        for div in div_list:
            item = ImgsproItem()
            img_name = div.xpath('./img/@alt').extract()
            img_name = ''.join(img_name) + '.jpg'
            item['img_name'] = img_name
            img_src = div.xpath('./img/@data-original').extract()
            img_src = 'https:' + ''.join(img_src)
            # 去掉_s以获取高清原图，如果链接里面有_s是缩略图
            s = re.sub('_s', '', img_src)
            item['img_src'] = s

            yield item
    # 另一种分页操作
        if self.page_num <= 3:
            new_url = f'https://sc.chinaz.com/tupian/index_{self.page_num}.html'
            self.page_num += 1

            yield scrapy.Request(new_url, callback=self.parse)