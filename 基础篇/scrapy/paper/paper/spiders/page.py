import scrapy


class PageSpider(scrapy.Spider):
    name = 'page'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919']

    def start_requests(self):
        url = 'https://passport.17k.com/ck/user/login'
        username = ''
        password = ''

        # 发送post的方案
        yield scrapy.FormRequest(
            url=url,
            formdata={
                'loginName': username,
                'password': password
            },
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        yield scrapy.Request(url=self.start_urls[0], callback=self.detail_parse)

    def detail_parse(self, response):
        print(response.json())