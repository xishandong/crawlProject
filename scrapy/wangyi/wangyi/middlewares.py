# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from .fake_useragent import USER_AGENTS
from scrapy.http import HtmlResponse
from time import sleep


class WangyiDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        # UA伪装
        request.headers['User-Agent'] = random.choice(USER_AGENTS)
        return None

    def process_response(self, request, response, spider):
        # 挑选出指定的响应对象进行篡改
        # 通过url指定request，通过request指定response
        # 获取动态加载出的动态数据，基于selenium
        bro = spider.bro

        if request.url in spider.models_url:
            # 五大板块对应的响应对象
            # 针对定位到的这些response进行篡改
            # 实例化一个新响应对象，包含动态加载的新闻数据，用新的换旧的
            bro.get(request.url)
            sleep(0.5)
            bro.execute_script('window.scrollTo(0,10000)')
            page_text = bro.page_source
            # self.fp = open('./news.html', 'w', encoding='utf-8')
            # self.fp.write(page_text)
            # self.fp.close()
            new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)

            return new_response
        else:
            # 其他请求对应的响应对象
            return response

    def process_exception(self, request, exception, spider):
        pass
