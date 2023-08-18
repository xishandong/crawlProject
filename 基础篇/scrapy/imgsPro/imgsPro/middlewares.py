# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ImgsproSpiderMiddleware:
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


class ImgsproDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# 中间件1 -随机UA
from .fake_useragent import get_requests_headers


class imgsProRandomuaDownloaderMiddleware(object):
    def process_request(self, request, spider):
        headers = get_requests_headers()
        request.headers['User-Agent'] = headers
        # print(agent)


# 中间件2 -随机代理
# import random
# from .proxies import proxy_list
#
# class BossjobRandomProxyDownloadMiddleware(object):
#     def process_requset(self, request, spider):
#         proxy = random.choice(proxy_list)
#         request.meta['proxy'] = proxy
#         print(proxy)
#
#     def process_exception(self, request, exception, spider):
#         # 处理代理ip无法使用情况
#         return request

# 中间件3 -Cookie
class imgsProCookieDownloaderMiddleware(object):
    def process_request(self, request, spider):
        cookie_dict = self.get_cookies()
        request.cookies = cookie_dict
        # print(cookie_dict)

    def get_cookies(self):
        cookie_string = 'cz_statistics_visitor=6a89d058-1928-b3b0-23ec-dd69be6c601a; __bid_n=184bced47869fe68784207; FPTOKEN=aJKftmn/cRusAPgCcLDE2nPw1f6AOJ8O2QUSZDc3c8DvI5BXZ30JDOFLJMgL1IRmUrXBPceos2w32lBfN2EV9YGfaTCJRsiUCa0hhZE/W7lV1yrRpNcTOHVpdJ+2coFSRUj1ah8fG8R959GOo63vzd2UuGRfjD+wf8giIlSk1FhVeFN28vpeiCScpwb6K6NH3Lu28AA/1idjRk6PUvVjZuUkUVAOb3zgBUtIvIlFH3Fy6PxnN0MYEFUBlXfGw+S5GRRrffN44WeiC1NzodYwUs78bOaxu6NxOp6a0LkOgoaWjCiGlF2sFTQNoOVMQcf3QZ+EGXVyKbhi1+YEmY4YrMMcQTkDgZGWtUlwhzkBjOi3pf8rT3axAIefUN12FZ7/D3D0tW59zkrNXqNNVbwPsg==|pnNJ+7La9ur/GH7QYr2dOE2BpmC7rfTIjxxwS6VDPJA=|10|1e90646f2dfd14de2376168eeb9968f4'
        cookie_dict = {}
        for kv in cookie_string.split(';'):
            k = kv.split('=')[0]
            v = kv.split('=')[1]
            cookie_dict[k] = v
        return cookie_dict

