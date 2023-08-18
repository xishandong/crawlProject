import json
from urllib.parse import urlencode
import scrapy
from ..fake_useragent import get_requests_headers
from ..fake_useragent import get_ua
from ..items import YicheItem
import time
from hashlib import md5
import math
import random
from scrapy.linkextractors import LinkExtractor
from copy import deepcopy
from ..test import detail


class CarSpider(scrapy.Spider):
    name = 'car'
    # allowed_domains = ['yiche.com']
    start_urls = ['https://car.yiche.com/']
    par = None  # 用来接受新车产生的params
    flag = 0  # 用来处理翻页的情况

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, headers=get_requests_headers())

    def UnlockHeaders(self):
        timestamp = str(int(time.time() * 1000))
        timestamp1 = str(int(time.time()))
        n = "cid=" + '508' + "&param=" + self.par + '19DDD1FBDFF065D3A4DA777D2D7A81EC' + timestamp

        # 标准的md5算法
        obj = md5()
        obj.update(n.encode('utf-8'))
        sign = obj.hexdigest()

        e = str(int(math.floor(9e8 * random.random()) + 1e8))

        headers = {
            'User-Agent': get_ua(),
            'cookie': f'locatecity=510500; bitauto_ipregion=118.120.163.142%3A%E5%9B%9B%E5%B7%9D%E7%9C%81%E6%B3%B8%E5%B7%9E%E5%B8%82%3B2517%2C%E6%B3%B8%E5%B7%9E%E5%B8%82%2Cluzhou; auto_id=1379418d938c31e5b46c80341902f496; CIGDCID=hF2wCGSy6NTNtynCkB6XESPQ3AY4KZBZ; CIGUID=8782b007-6016-43c6-bbfc-884006db6193; selectcity=510500; selectcityid=2517; selectcityName=%E6%B3%B8%E5%B7%9E; UserGuid=8782b007-6016-43c6-bbfc-884006db6193; Hm_lvt_610fee5a506c80c9e1a46aa9a2de2e44=1673438164,1673490111; csids=2593_5536_5476_4322_1661; report-cookie-id={e}_{timestamp}; Hm_lpvt_610fee5a506c80c9e1a46aa9a2de2e44={timestamp1}',
            'refer': 'https://car.yiche.com/',
            'content-type': 'application/json;charset=UTF-8',
            'x-city-id': '2517',
            'x-ip-address': '118.120.163.142',
            'x-platform': 'pc',
            'x-sign': sign,  # 需要逆向开发
            'x-timestamp': timestamp,  # 需要逆向开发，当前系统时间（数字）
            'x-user-guid': '8782b007-6016-43c6-bbfc-884006db6193'  # 从cookie中暂时复制过去
        }
        return headers

    # 这个请求得到了所有的汽车品牌
    def parse(self, response, **kwargs):
        div_list = response.xpath('//div[@class="brand-list-content"]/div/div')  # 拿到了A~Z·汽车品牌标签
        for div in div_list:
            brand_list = div.xpath('./div[@class="item-brand"]')  # 拿到了A~Z标签中的汽车详情
            for br in brand_list:
                item = YicheItem()
                brand = br.xpath('./a/div/text()').extract_first().strip()
                brand_src = 'https://car.yiche.com' + br.xpath('./a/@href').extract_first()
                item['brand'] = brand
                yield scrapy.Request(
                    meta={'item': item},
                    headers=get_requests_headers(),
                    url=brand_src,
                    callback=self.brandCar_parse
                )
            #     break  # 放开这个得到某个英文字母开头的所有汽车品牌
            # break  # 放开这个得到所有英文字母开头的品牌

    # 这个请求得到了汽车品牌中的汽车名字和id
    def brandCar_parse(self, response):
        # 控制翻页
        if self.flag == 2:
            self.flag = 0

        div_list = response.xpath('//div[@class="search-result-list"]/div')
        item = response.meta['item']

        # 处理没有车的情况
        if not div_list:
            item['car_name'] = item['brand']
            item['car_num'] = '暂无在售车辆'
            item['car_detail'] = '暂无在售车辆'
            item['car_name1'] = '暂无在售车辆'
            yield item

        for div in div_list:
            carNum = div.xpath('./@data-id').extract_first()
            carNam = div.xpath('./a/p[1]/text()').extract_first()
            item['car_name'] = carNam
            item['car_num'] = carNum
            dic = '{"cityId":"2517","serialId":"%d"}'
            p = format(dic % int(carNum))
            self.par = p  # 将参数传给类
            params = {
                'cid': '508',
                'param': p
            }
            url = "https://mapi.yiche.com/web_api/car_model_api/api/v1/car/config_new_param?" + urlencode(params)

            yield scrapy.Request(
                meta={'item': deepcopy(item)},
                url=url,
                headers=self.UnlockHeaders(),
                callback=self.peizhi_parse
            )
            # break  # 这个控制输出车的数量

        # 判断翻页
        link = LinkExtractor(allow=r'mid=\d&page=\d').extract_links(response)
        if link:
            try:
                next_url = link[self.flag].url
            except:
                next_url = link[0].url
            self.flag += 1
            yield scrapy.Request(
                meta={'item': deepcopy(item)},
                headers=get_requests_headers(),
                url=next_url,
                callback=self.brandCar_parse
            )

    # 这个请求得到了汽车的详细详细，得到的是json文件
    def peizhi_parse(self, response):
        item = response.meta['item']
        res = json.loads(response.text)
        data = [res['data']]
        # 需要处理没有公开参数的车
        if data == [[]]:
            item['car_detail'] = "参数配置暂未公开"
            item['car_name1'] = '暂无在售车辆'
        # 处理参数公开的车
        else:
            car = detail(response.text)
            item['car_detail'] = car['detail']
            item['car_name1'] = car['name']
        yield item
