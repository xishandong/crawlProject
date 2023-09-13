import json
import time
from csv import DictWriter
from itertools import islice
from typing import Literal, Iterator, Union
from urllib.parse import urlparse, parse_qs

import execjs
import requests
from lxml import etree
from tqdm import tqdm

# ip代理信息
from Proxy_info import proxies, get_api
from boss.点选 import BossSlide

# 类型控制
Accept = Literal['json', 'text', 'contents']
city_code_dict: dict = json.load(open('cityCode.json', 'r', encoding='utf-8'))

# 休眠时间
sleepTime = 5


class BossJob:
    def __init__(self, js_name: str = '', proxy: dict = None):
        self.isFirst: bool = True  # 是否为初次访问
        self.js_name: str = js_name  # js的名称
        self.seed: str = ''  # 随机种子
        self.ts: str = ''  # 时间戳
        # api列表
        self.apiList: list[str] = [
            'https://www.zhipin.com/wapi/zpgeek/mobile/search/joblist.json',  # 职位搜索页, 需要指定params
            'https://www.zhipin.com/job_detail/',  # 不需要指定params
            f'https://www.zhipin.com/web/common/security-js/{self.js_name}.js',  # 动态加载js的链接
            'https://www.zhipin.com/wapi/zpgeek/search/joblist.json'  # web api
        ]
        # 请求头
        self.headers: dict = {
            'Accept': 'application/json, text/plain, */*',
        }
        self.cookies: dict = {}  # cookie
        self.js = execjs.compile(open('demo.js', 'r', encoding='utf-8').read())  # 调用的js
        self.stop: bool = False  # 控制手机端搜索停止
        self.checkEnd: str = ''  # 检测手机端是否爬完
        self.proxy = proxy  # 代理

    # 发送请求
    def ajax_request(self, url: str, params: dict = None, cookies=None) -> requests.Response:
        for _ in range(5):
            try:
                resp = requests.get(url, params=params, headers=self.headers, cookies=cookies, timeout=10,
                                    proxies=self.proxy)
                if resp.status_code == 200:
                    return resp
                elif resp.status_code == 403:
                    print("=====出现响应码403, ip被封=====")
                    self.show_pro(sleepTime)
                    self.change_ip()
                    continue
                else:
                    print('HTTP Error: %s' % resp.status_code)
                    self.show_pro(sleepTime)
                    continue

            except Exception as e:
                print('出现错误: ', e)
                print('链接为: ', url)
                self.show_pro(sleepTime)
                continue
        else:
            raise Exception('超过5次也无法正常获取响应...')

    # 初始化搜索
    def first_get_seed(self, url: str, params: dict = None, isWeb: bool = False) -> Union[requests.Response, None]:
        if self.isFirst:
            resp = self.ajax_request(url=url, params=params)
            self.isFirst = False
        else:
            resp = self.ajax_request(url=url, params=params, cookies=self.cookies)
        # 未发生重定向以及是web端的情况
        if resp.url == url and not isWeb:
            print(f'=====本次没有更新cookie: {resp.url} =====')
            return resp
        elif isWeb:
            zpData = resp.json()['zpData']
            self.seed = zpData['seed']
            self.ts = zpData['ts']
            name = zpData['name']
            self.check_js(name)
            return
        # 处理重定向到检查页面的情况
        parsedUrl = urlparse(resp.url)
        generatedDict = parse_qs(parsedUrl.query)
        self.seed = generatedDict['seed'][0]
        self.ts = generatedDict['ts'][0]
        name = generatedDict['name'][0]
        self.check_js(name)

    # 手机端搜索职位
    def search_job_mobile(self, position: str, city: str, startPage: int = 1) -> Iterator:
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        })
        city_code = city_code_dict.get(city)
        if city_code:
            params: dict = {
                'city': city_code,
                'query': position,
                'page': startPage
            }
            # 初始化搜索
            self.first_get_seed(self.apiList[1], params)
            self.update_cookie()
            continuations: list = [params]
            # 模拟翻页
            while continuations:
                continuation = continuations.pop()
                resp = self.ajax_request('https://www.zhipin.com/wapi/zpgeek/mobile/search/joblist.json',
                                         params=continuation, cookies=self.cookies)
                html = resp.json().get('zpData', {}).get('html')
                # 存在新的帖子
                if html and self.stop is False:
                    print(f'=====爬取{position}-{city}第{continuation["page"]}页=====')
                    continuation['page'] += 1
                    continuations.append(continuation)
                    # 提交数据
                    yield from self.parse_search_html(html)
                    # 控制爬取频率
                    self.show_pro(sleepTime)
                elif not html and self.stop is False:
                    print('=====ip被封=====')
                    continuations.append(continuation)
                    self.show_pro(sleepTime)
                    self.change_ip()
                    self.isFirst = True
                    self.first_get_seed(self.apiList[1], params)
                    self.update_cookie()
                else:
                    print(f'=====爬取{position}-{city}停止=====')
        else:
            raise Exception(f'错误的城市名称: {city}')

    # web端搜索
    def search_job_web(self, position: str, city: str, startPage: int = 1, totalPage: int = 1) -> Iterator:
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        })
        city_code = city_code_dict.get(city)

        if city_code:
            params = {
                'query': position,
                'city': city_code,
                'page': 1,
                'pageSize': '30',
                'scene': '1',
            }
            # 初次访问
            self.isFirst = True
            self.first_get_seed(self.apiList[3], params=params, isWeb=True)
            page = startPage
            # 控制翻页
            while page <= totalPage:
                params.update({'page': page})
                self.update_cookie()
                resp = self.ajax_request(self.apiList[3], params=params, cookies=self.cookies)

                print(f'=====爬取{position}-{city}第{page}页=====')
                # 出现访问异常，重新生成cookie
                if resp.json().get('code') == 37:
                    print(f'====={resp.json().get("message")}, 正在重试 =====')
                    zpData = resp.json()['zpData']
                    self.seed = zpData['seed']
                    self.ts = zpData['ts']
                    self.show_pro(sleepTime)
                    continue
                # 出现ip被封，暂停一下
                elif resp.json().get('code') == 5002:
                    print(f'====={resp.json().get("message")}=====')
                    self.show_pro(sleepTime)
                    self.change_ip()
                    self.isFirst = True
                    self.first_get_seed(self.apiList[3], params=params, isWeb=True)
                    continue
                # 得到数据
                searchData = resp.json().get('zpData', {}).get('jobList')
                if searchData:
                    page += 1
                    # 提交管道
                    yield from self.parse_search_data(searchData)
                    # 休息一下
                    self.show_pro(sleepTime)
                # 获取下一次访问所需种子和时间戳
                self.seed = resp.cookies['__zp_sseed__']
                self.ts = resp.cookies['__zp_sts__']
        else:
            raise Exception(f'错误的城市名称: {city}')

    # 获取详情页
    def get_job_details_by_id(self, encryptJobId: str) -> str:
        url = self.apiList[1] + encryptJobId + '.html'
        return self.get_job_details_bt_url(url)

    # 获取详情页
    def get_job_details_bt_url(self, url: str) -> str:
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        })
        resp = self.first_get_seed(url)
        self.update_cookie()

        if not resp:
            resp = self.ajax_request(url, cookies=self.cookies)
        tree = etree.HTML(resp.text)
        texts = tree.xpath('//div[@class="detail-content"]//text()')
        textList: list = [i.strip() for i in texts if i.strip()]

        if not textList:
            print('===== 重置cookie获取详情页 =====')
            self.isFirst = True
            self.show_pro(sleepTime)
            return self.get_job_details_bt_url(url)

        return '\n'.join(textList)

    # 保存手机端搜索结果
    def save_job_list_to_csv(self, position: str, city: str, startPage: int = 1, saveCount: int = 100):
        dataSet: Iterator = self.search_job_mobile(position, city, startPage)

        header = ['job_name', 'detail_url', 'pay', 'company_name', 'requirement']
        fp = open(f'mobile-{position}-{city}.csv', 'w', encoding='utf-8', newline='')
        writer = DictWriter(fp, header)
        writer.writeheader()

        for job in islice(dataSet, saveCount):
            job['requirement'] = ';'.join(job['requirement'])
            writer.writerow(job)

    # 保存web端搜索结果
    def save_job_list_to_csv_web(self, position: str, city: str, startPage: int = 1, savePage: int = 2):
        dataSet = self.search_job_web(position, city, startPage, savePage)

        header = [
            'jobName', 'encryptJobId', 'salaryDesc', 'jobLabels', 'skills', 'jobExperience',
            'jobDegree', 'cityName', 'brandName', 'brandScaleName', 'welfareList', 'brandIndustry'
        ]
        fp = open(f'web-{position}-{city}.csv', 'w', encoding='utf-8', newline='')
        writer = DictWriter(fp, header)
        writer.writeheader()

        for job in dataSet:
            job['jobLabels'] = ';'.join(job['jobLabels'])
            job['skills'] = ';'.join(job['skills'])
            job['welfareList'] = ';'.join(job['welfareList'])
            writer.writerow(job)

    # 更新cookie
    def update_cookie(self):
        __zp = self.js.call('r', self.seed, self.ts)
        self.cookies['__zp_stoken__'] = __zp
        print(f'=====更新cookie: {self.cookies["__zp_stoken__"]}')

    # 解析手机端搜索
    def parse_search_html(self, html: str) -> Iterator:
        tree = etree.HTML(html)
        li_list = tree.xpath('//li')

        for num, li in enumerate(li_list, start=1):
            if num == 1:
                if self.checkEnd == li.xpath('./a/@href')[0]:
                    self.stop = True
                    return
                self.checkEnd = li.xpath('./a/@href')[0]

            yield {
                'job_name': li.xpath('./a/div[1]/span[1]/text()')[0],
                'detail_url': 'https://www.zhipin.com' + li.xpath('./a/@href')[0],
                'pay': li.xpath('a/div[1]/span[2]/text()')[0],
                'company_name': li.xpath('./a/div[2]/span[1]/text()')[0],
                'requirement': [r.strip() for r in li.xpath('./a/div[3]//text()') if r.strip()]
            }

    # 检查js是否为最新
    def check_js(self, name):
        if self.js_name != name:
            self.js_name = name
            print(f"=====这次的js名称 -----> {name} =====")
            resp = self.ajax_request(f'https://www.zhipin.com/web/common/security-js/{self.js_name}.js').text
            resp_ = resp.split('module,')
            resp = ''

            # 对 module 进行处理，否则容易识别为爬虫
            for i in range(len(resp_)):
                resp += resp_[i]
                if i == 0:
                    resp += 'module_,'
                if i == 1:
                    resp += 'module,'

            with open('./jssss.js', 'w', encoding='utf-8') as f:
                f.write(resp)

    @staticmethod
    # 解析web端搜索结果
    def parse_search_data(searchData: list[dict]) -> Iterator:
        for job in searchData:
            yield {
                'jobName': job['jobName'],
                'encryptJobId': job['encryptJobId'],
                'salaryDesc': job['salaryDesc'],
                'jobLabels': job['jobLabels'],
                'skills': job['skills'],
                'jobExperience': job['jobExperience'],
                'jobDegree': job['jobDegree'],
                'cityName': job['cityName'],
                'brandName': job['brandName'],
                'brandScaleName': job['brandScaleName'],
                'welfareList': job['welfareList'],
                'brandIndustry': job['brandIndustry']
            }

    @staticmethod
    def change_ip():
        BossSlide().verify()

    @staticmethod
    # 展示休息进度条
    def show_pro(t: int, isOpen: bool = True):
        pass
        # time.sleep(1)
        # if isOpen:
        #     for _ in tqdm(
        #             range(t * 10),
        #             leave=False,
        #             colour='blue',
        #             desc='正在等待中...',
        #             ascii='*-'
        #     ):
        #         time.sleep(0.1)


if __name__ == '__main__':
    boss = BossJob('8955eed0', proxy=proxies)
    # 通过url获取详情页
    # detail = boss.get_job_details_bt_url('https://www.zhipin.com/job_detail/fc823036861698e10nF42NW0GVo~.html')
    # 通过加密id获取详情页
    # detail = boss.get_job_details_by_id('05988daddc5b6afc1n1-3du1FVZW')
    # print(detail)
    # 保存数据
    # boss.save_job_list_to_csv('python', '上海', saveCount=20)
    # boss.save_job_list_to_csv_web('python', '上海', 2, 2)
    # web搜索
    items = boss.search_job_web('python', '上海', 1, 10)
    # mobile搜搜
    # items = boss.search_job_mobile('web', '上海')
    for item in items:
        print(item)
