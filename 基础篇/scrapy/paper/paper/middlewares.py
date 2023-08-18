# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from .fake_useragent import get_ua


class PaperDownloaderMiddleware:

    def process_request(self, request, spider):
        # UA伪装
        headers = get_ua()
        request.headers['User-Agent'] = headers
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass


class CookieDownloaderMiddleware(object):
    def process_request(self, request, spider):
        cookie_dict = self.get_cookies()
        request.cookies = cookie_dict

    def get_cookies(self):
        # cookie_string = ''
        cookie_string = ''
        cookie_dict = {}
        for kv in cookie_string.split(';'):
            k = kv.split('=')[0]
            v = kv.split('=')[1]
            cookie_dict[k] = v
        return cookie_dict
