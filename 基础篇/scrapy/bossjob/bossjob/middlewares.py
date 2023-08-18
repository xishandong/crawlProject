# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
# useful for handling different item types with a single interface
# 中间件1 -随机UA
from scrapy.http import HtmlResponse

from .fake_useragent import get_ua
from .requset import SeleniumRequest


class BossjobRandomuaDownloaderMiddleware(object):
    def process_request(self, request, spider):
        headers = get_ua()
        request.headers['User-Agent'] = headers
        return None


# 中间件2 -随机代理


class BossjobRandomProxyDownloadMiddleware(object):
    def process_request(self, request, spider):
        proxy = "u286.kdltps.com:15818"

        # 用户名密码认证
        username = "t17335887797243"
        password = "n62s2uvp"
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                                        "proxy": proxy}

        # 白名单认证
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}

        request.headers["Connection"] = "close"
        return None


# 中间件3 -Cookie


class BossjobCookieDownloaderMiddleware(object):

    def process_request(self, request, spider):
        cookie_dict = self.get_cookies()
        request.cookies = cookie_dict
        return None

    def get_cookies(self):
        cookie_string = 'wd_guid=544d13f9-f072-4fdc-9989-84452f1ecd52; historyState=state; _bl_uid=XtlO5cqLjv05qpj3t0d0nna8msI4; lastCity=101020100; wt2=DY4IX_Pe18l5jPqD0AYgnA-G9UnTNtDaZ_zMhCpK7UovHjn5bKxYiZ6NtwTrfsFzsgpxFtIBCopvwd7HdvXTGrg~~; wbg=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1673257271,1673333037,1673421249,1673621120; __g=-; __l=l=%2Fwww.zhipin.com%2Fjob_detail%2F01fd3a4e0ace71af1nx_0t-1F1pZ.html&s=3&friend_source=0&s=3&friend_source=0; geek_zp_token=V1RN0kEOL031ZiVtRvyB4eKymy7j3Vwi4~; __c=1673621123; __a=68265253.1672926940.1673421249.1673621123.475.11.15.475; __zp_stoken__=357feaV5aXwJLbUlmOy4uTW43dBlpeEsAbV5LT1RBZ10vQAMUSG4OBXFMIDkiIkJ0D3Z%2Bb35WOlduHEoVLlt3bnRiWQNiGnw7AgQdWhkjdlJNETohVUMiZCUfHx8IKAQ%2FTU9MDi1fN3RRXTk%3D; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1673621689'
        cookie_dict = {}
        for kv in cookie_string.split(';'):
            k = kv.split('=')[0]
            v = kv.split('=')[1]
            cookie_dict[k] = v
        return cookie_dict


import zipfile
import string
from selenium import webdriver


class seleniumDownloaderMiddleware(object):

    def __init__(self):
        self.option = webdriver.ChromeOptions()

        def create_proxyauth_extension(tunnelhost, tunnelport, proxy_username, proxy_password, scheme='http',
                                       plugin_path=None):
            if plugin_path is None:
                plugin_path = 'vimm_chrome_proxyauth_plugin.zip'

            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js逆向"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

            background_js = string.Template(
                """
                var config = {
                        mode: "fixed_servers",
                        rules: {
                        singleProxy: {
                            scheme: "${scheme}",
                            host: "${host}",
                            port: parseInt(${port})
                        },
                        bypassList: ["foobar.com"]
                        }
                    };

                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "${username}",
                            password: "${password}"
                        }
                    };
                }

                chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                );
                """
            ).substitute(
                host=tunnelhost,
                port=tunnelport,
                username=proxy_username,
                password=proxy_password,
                scheme=scheme,
            )
            with zipfile.ZipFile(plugin_path, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js逆向", background_js)
            return plugin_path

        proxyauth_plugin_path = create_proxyauth_extension(
            tunnelhost="u286.kdltps.com",  # 隧道域名
            tunnelport="15818",  # 端口号
            proxy_username="t17335887797243",  # 用户名
            proxy_password="n62s2uvp"  # 密码
        )
        self.option.add_extension(proxyauth_plugin_path)
        # elf.option.add_argument('--headless')
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_experimental_option('useAutomationExtension', False)
        self.option.add_argument('blink-settings=imagesEnabled=false')
        self.option.add_argument("--no-sandbox")
        self.option.add_argument("--disable-dev-shm-usage")
        self.option.add_argument('--disable-gpu')
        self.bro = webdriver.Chrome(executable_path='D:\爬虫\selenium\chromedriver.exe', options=self.option)
        self.bro.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })

    def __del__(self):
        self.bro.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.__del__, signal=signals.spider_closed)
        return s

    def process_request(self, spider, request):
        # 所有的请求都会到这里，判断是否需要selenium来处理请求
        if isinstance(request, SeleniumRequest):
            # selenium操作
            self.bro.get(request.url)
            time.sleep(2)
            page_text = self.bro.page_source
            return HtmlResponse(url=request.url, status=200, body=page_text, request=request, encoding='utf-8')
        else:
            return None
