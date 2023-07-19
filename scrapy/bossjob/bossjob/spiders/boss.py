import json

import scrapy
from lxml import etree

from ..items import BossjobItem


class BossSpider(scrapy.Spider):
    name = 'boss'

    def start_requests(self):
        for pageNum in range(51, 90):
            url = f'https://www.zhipin.com/wapi/zpgeek/mobile/search/joblist.json?page={pageNum}&city=101020100&query='
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        res = json.loads(response.text)
        it = {'html': res['zpData']['html']}
        tree = etree.HTML(it['html'])
        li_list = tree.xpath('//li')

        for li in li_list:
            item = BossjobItem()
            job_name = li.xpath('./a/div[1]/span[1]/text()')[0]
            item['job_name'] = job_name
            detail_url = 'https://www.zhipin.com' + li.xpath('./a/@href')[0]
            item['detail_url'] = detail_url
            pay = li.xpath('a/div[1]/span[2]/text()')[0]
            item['pay'] = pay
            company_name = li.xpath('./a/div[2]/span[1]/text()')[0]
            item['company_name'] = company_name
            requirement = li.xpath('./a/div[3]//text()')
            re = ''
            for i in range(1, len(requirement)):
                re = re + requirement[i].strip() + ' '
            item['requirement'] = re

            yield item
