# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from time import sleep

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse


class SunproSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SunproDownloaderMiddleware:
    def process_response(self, request, response, spider):
        # 挑选出指定的响应对象进行篡改
        # 通过url指定request，通过request指定response
        # 获取动态加载出的动态数据，基于selenium
        bro = spider.bro
        bro.get(request.url)
        sleep(0.1)
        page_text = bro.page_source
        new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)

        return new_response


# 中间件1 -随机UA
from .fake_useragent import get_requests_headers


class RandomuaDownloaderMiddleware(object):
    def process_request(self, request, spider):
        headers = get_requests_headers()
        request.headers['User-Agent'] = headers
        # print(agent)


# 中间件2 -随机代理
# import random
# from .proxies import proxy_list
#
# class RandomProxyDownloadMiddleware(object):
#     def process_requset(self, request, spider):
#         proxy = random.choice(proxy_list)
#         request.meta['proxy'] = proxy
#         print(proxy)
#
#     def process_exception(self, request, exception, spider):
#         # 处理代理ip无法使用情况
#         return request

# 中间件3 -Cookie
class CookieDownloaderMiddleware(object):
    def process_request(self, request, spider):
        cookie_dict = self.get_cookies()
        request.cookies = cookie_dict
        # print(cookie_dict)

    def get_cookies(self):
        cookie_string = 'tgw_l7_route=581a2b818047111abece09009aea53ba; PHPSESSID=6sq7bpo9m0vsntmr1mq7othflj; Hm_lvt_8634401b25f1b0008d9638ccfc17752d=1673232337; Hm_lvt_3ac08b9ee936f8dd8b720065d8af23d0=1673232337; Hm_lpvt_3ac08b9ee936f8dd8b720065d8af23d0=1673233037; Hm_lpvt_8634401b25f1b0008d9638ccfc17752d=1673233037'
        cookie_dict = {}
        for kv in cookie_string.split(';'):
            k = kv.split('=')[0]
            v = kv.split('=')[1]
            cookie_dict[k] = v
        return cookie_dict
