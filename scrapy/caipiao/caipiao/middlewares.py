# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from time import sleep

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse

from .fake_useragent import USER_AGENTS


class CaipiaoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        # UA伪装
        request.headers['User-Agent'] = random.choice(USER_AGENTS)
        return None

    def process_response(self, request, response, spider):
        bro = spider.bro
        bro.get(request.url)
        sleep(0.5)
        click = bro.find_element_by_xpath('//*[@id="link248"]/img').click()
        start = bro.find_element_by_id('from')
        start.clear()
        start.send_keys('16001')
        end = bro.find_element_by_id('to')
        end.clear()
        end.send_keys('23004')
        find = bro.find_element_by_id('link176').click()
        page_text = bro.page_source
        new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)

        return new_response

    def process_exception(self, request, exception, spider):

        pass
