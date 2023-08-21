import hashlib
import json
import time
from typing import Iterator
from urllib.parse import urlencode

import requests
from playwright.sync_api import sync_playwright

HTML_FILEPATH: str = 'file://D:/crawlProjects/饿了么/hello.html'

URLS = [
    'https://waimai-guide.ele.me/h5/mtop.alsc.eleme.miniapp.homepagev1/1.0/5.0/',
    'https://waimai-guide.ele.me/h5/mtop.relationrecommend.tinyapprecommend.loginrecommend/1.0/5.0/'
]


class EleMe:
    headers: dict = {
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    cookies: dict = {
        '_m_h5_tk': '',
        '_m_h5_tk_enc': '',
        'cookie2': '',
        'USERID': ''
    }

    def __init__(self):
        self.stop_search: bool = False

    def ajax_request(self, url, params, retryTimes: int = 5) -> requests.Response:
        for _ in range(retryTimes):
            try:
                response = requests.get(url, params=params, headers=self.headers, cookies=self.cookies)
                if response.status_code == 200:
                    return response
            except requests.exceptions.RequestException as e:
                print(e)
                print(f'retrying request: {_}/{retryTimes}...')
                continue
        else:
            raise Exception(f'after {retryTimes} times, still can not retrieve response')

    def from_params(self, url: str, data: str) -> dict:
        token = self.cookies['_m_h5_tk'].split('_')[0]
        t = str(int(time.time() * 1000))
        appKey = '12574478'
        md5_hash_obj = hashlib.md5()
        text = token + "&" + t + "&" + appKey + "&" + data
        md5_hash_obj.update(text.encode('utf-8'))
        sign = md5_hash_obj.hexdigest()
        params = {
            'jsv': '2.7.2',
            'appKey': appKey,
            't': t,
            'sign': sign,
            'api': url.split('/')[4],
            'v': '1.0',
            'dataType': 'json',
            'mainDomain': 'ele.me',
            'subDomain': 'waimai-guide',
            'pageDomain': 'ele.me',
            'H5Request': 'true',
            'ttid': 'h5@Web_iphone_10.30.0',
            'type': 'originaljson',
            'SV': '5.0',
            'data': data
        }
        v = url.replace('https:', '') + '?' + urlencode(params)
        params['bx_et'] = self.get_etSign(v)
        return params

    def get_home_recommend(self) -> Iterator:
        url = URLS[0]
        data = self.first_home_recommend_query()
        continuations: list[str] = [data]
        offset: int = 0
        while continuations:
            continuation = continuations.pop()
            params = self.from_params(url, continuation)
            response = self.ajax_request(url, params=params)
            data = response.json().get('data', {}).get('data')
            homeRecommend = data.get('frontend_page_shop_list_recommend', {})
            rankId = homeRecommend.get('customized', {}).get('rankId')
            _items = homeRecommend.get('fields', {}).get('items')
            if rankId and _items:
                offset += len(_items)
                continuations.append(self.next_home_recommend_query(rankId, offset))
            yield from self.parse_home_recommend(_items)

    def get_search_results(self, keyword: str) -> Iterator:
        url = URLS[1]
        data = self.first_search(keyword)
        continuations: list[str] = [data]
        offset = 0
        page = 1
        while continuations:
            continuation = continuations.pop()
            params = self.from_params(url, continuation)
            response = self.ajax_request(url, params)
            data = response.json().get('data', {}).get('result', {})
            if isinstance(data, list):
                data = data[0]
            listItem = data.get('listItems', [])
            rankId = data.get('pageInfo', {}).get('rankId')
            if listItem and rankId and self.stop_search is False:
                offset += len(listItem)
                page += 1
                continuations.append(self.next_search(keyword, offset, page, rankId))
            yield from self.parse_search_data(listItem)

    def parse_search_data(self, datas: list) -> Iterator:
        for data in datas:
            restaurant: dict = data.get('restaurant')
            foods: list[dict] = data.get('foods', [])
            title = data.get('title')
            if title == '搜索结果较少，为你推荐更多内容':
                self.stop_search: bool = True
            if foods:
                foods = [{
                    'skuIdStr': food.get('skuIdStr'),
                    'foodId': food.get('foodId'),
                    'name': food.get('name'),
                    'description': food.get('description'),
                    'schemeId': food.get('schemeId'),
                    'predictPrice': food.get('predictPrice'),
                    'price': food.get('price'),
                    'itemId': food.get('itemId'),
                    'skuId': food.get('skuId'),
                    'itemIdStr': food.get('itemIdStr'),
                    'categoryId': food.get('categoryId'),
                    'eleItemId': food.get('eleItemId')
                } for food in foods]
            if restaurant:
                yield {
                    'id': restaurant.get('id'),
                    'name': restaurant.get('name'),
                    'brandName': restaurant.get('brandName'),
                    'brandId': restaurant.get('brandId'),
                    'cover': restaurant.get('imagePath'),
                    'rating': restaurant.get('rating'),
                    'recentOrderNumDisplay': restaurant.get('recentOrderNumDisplay'),
                    'averagePrice': restaurant.get('averagePrice'),
                    'praiseCount': restaurant.get('praiseCount'),
                    'targetTagPath': restaurant.get('targetTagPath'),
                    'schemeId': restaurant.get('schemeId'),
                    'openingHours': restaurant.get('openingHours'),
                    'rules': restaurant.get('piecewiseAgentFee', {}).get('rules'),
                    'foods': foods
                }

    def first_search(self, keywords: str) -> str:
        params = {
            "appId": "77",
            "_input_charset": "UTF-8",
            "_output_charset": "UTF-8",
            "gatewayApiType": "mtop",
            "x-ele-scene": "search",
            "mtop_api_version": "1.0",
            "platform": "999",
            "alipayChannel": 1,
            "sversion": "4.0",
            "limit": 5,
            "n": 5,
            "page": 1,
            "searchMode": 1,
            "userId": self.cookies['USERID'],
            "latitude": "28.864343",
            "longitude": "105.407142",
            "keyword": keywords,
            "refer": "直接搜索"
        }
        data = {
            "appId": "77",
            "type": "originaljson",
            "params": json.dumps(params, separators=(',', ':'), ensure_ascii=False),
        }
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

    def next_search(self, keywords: str, offset: int, page: int, rankId: str) -> str:
        params = {
            "appId": "77",
            "_input_charset": "UTF-8",
            "_output_charset": "UTF-8",
            "gatewayApiType": "mtop",
            "x-ele-scene": "search",
            "mtop_api_version": "1.0",
            "platform": "999",
            "alipayChannel": 1,
            "sversion": "4.0",
            "limit": 5,
            "n": 5,
            "page": page,
            "searchMode": 1,
            "userId": self.cookies['USERID'],
            "latitude": "28.864343",
            "longitude": "105.407142",
            "keyword": keywords,
            "refer": "直接搜索",
            "offset": offset,
            "rankId": rankId,
        }
        data = {
            "appId": "77",
            "type": "originaljson",
            "params": json.dumps(params, separators=(',', ':'), ensure_ascii=False),
        }
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

    @staticmethod
    def first_home_recommend_query() -> str:
        queryParams = {
            "id": "",
            "description": "",
            "title": "附近推荐",
            "tabName": "%E9%99%84%E8%BF%91%E6%8E%A8%E8%8D%90",
            "pageCode": "MINIAPP_ELEME_HOME_LIST",
            "pageType": "",
            "clickAfterColor": "#00a6ff",
            "clickBeforeColor": "#333",
            "fontWeight": "bold",
            "listType": "",
            "position": 1,
            "scrollTop": 0,
            "tabCode": "recommend_tab"
        }
        pageParams = {
            "offset": 0,
            "rankId": "",
            "behavior": "expose_list%24%24___click_list%24%24",
            "queryParams": json.dumps(queryParams, separators=(',', ':'), ensure_ascii=False),
            "limit": 5,
            "scene": "miniapp:homepage"
        }
        data = {
            "sceneCode": "MINIAPP_ELEME_HOME_LIST",
            "needReverseGeoAddress": 1,
            "pageParams": json.dumps(pageParams, separators=(',', ':'), ensure_ascii=False),
            "longitude": "105.407142",
            "latitude": "28.864343"
        }
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

    @staticmethod
    def next_home_recommend_query(rankId: str, offset: int) -> str:
        queryParams = {
            "id": "",
            "description": "",
            "title": "附近推荐",
            "tabName": "%E9%99%84%E8%BF%91%E6%8E%A8%E8%8D%90",
            "pageCode": "MINIAPP_ELEME_HOME_LIST",
            "pageType": "",
            "clickAfterColor": "#00a6ff",
            "clickBeforeColor": "#333",
            "fontWeight": "bold",
            "listType": "",
            "position": 1,
            "scrollTop": 0,
            "tabCode": "recommend_tab"
        }
        pageParams = {
            "offset": offset,
            "rankId": rankId,
            "behavior": "expose_list%24%24___click_list%24%24",
            "queryParams": json.dumps(queryParams, separators=(',', ':'), ensure_ascii=False),
            "limit": 20,
            "scene": "miniapp:homepage"
        }
        data = {
            "eventAction": "nextPage",
            "sceneCode": "MINIAPP_ELEME_HOME_LIST",
            "componentCode": "frontend_page_shop_list_recommend",
            "longitude": "105.407142",
            "latitude": "28.864343",
            "needReverseGeoAddress": 0,
            "pageParams": json.dumps(pageParams, separators=(',', ':'), ensure_ascii=False),
            "logicPageId": "transformerpage_987"
        }
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

    @staticmethod
    def get_etSign(data: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # 打开本地网页
            page.goto(HTML_FILEPATH)
            # 调用本地网页中的方法
            etSign = page.evaluate(f'etSign("{data}")')
            browser.close()
            return etSign

    @staticmethod
    def parse_home_recommend(datas: list) -> Iterator:
        for data in datas:
            restaurant: dict = data.get('fields', {}).get('restaurant')
            if restaurant:
                yield {
                    'id': restaurant.get('id'),
                    'name': restaurant.get('name'),
                    'brandName': restaurant.get('brandName'),
                    'brandId': restaurant.get('brandId'),
                    'cover': restaurant.get('imagePath'),
                    'rating': restaurant.get('rating'),
                    'recentOrderNumDisplay': restaurant.get('recentOrderNumDisplay'),
                    'averagePrice': restaurant.get('averagePrice'),
                    'praiseCount': restaurant.get('praiseCount'),
                    'targetTagPath': restaurant.get('targetTagPath'),
                    'schemeId': restaurant.get('schemeId'),
                    'openingHours': restaurant.get('openingHours'),
                    'rules': restaurant.get('piecewiseAgentFee', {}).get('rules')
                }


if __name__ == '__main__':
    el = EleMe()

    items = el.get_search_results('麦当劳')
    # items = el.get_home_recommend()
    for i in items:
        print(i)
