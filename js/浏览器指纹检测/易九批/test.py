import time

import execjs
from curl_cffi import requests

timestamp = str(int(time.time()))


def getList():
    headers = {
        'Content-Type': 'application/json',
        'token': '',
    }
    json_data = {
        'data': {
            'zoneId': '4932265882383941446',
        },
        'cityId': '701',
        'userClassId': 1,
        'userDisplayClass': 0,
        'addressId': '',
        'deviceType': 3,
    }
    x_ = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('setHeader', 'POST',
                                                                            '/v54/ProductCategory/ListCategoryTree',
                                                                            json_data, timestamp)
    headers.update(x_)
    response = requests.post('https://www.yijiupi.com/v54/ProductCategory/ListCategoryTree', headers=headers,
                             json=json_data)
    print(response.json())


def getData():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
        'token': '',
    }
    json_data = {
        'data': {
            'sonCategoryId': '',
            'brandId': '',
            'firstCategoryId': '',
            'searchKey': '国台国酱',
            'specialAreaId': '',
            'categoryIds': [],
            'brandIds': [],
            'labelId': None,
            'isAscending': '',
            'searchModes': [
                2,
            ],
            'sort': 0,
            'shopId': '',
            'currentPage': 1,
            'pageSize': 60,
            'filterSpecialArea': False,
            'searchSource': 1,
            'warehouseIds': [],
            'searchKeyNotCorrect': False,
            'couponTemplateId': '',
            'channelId': '',
        },
        'cityId': '701',
        'userClassId': 1,
        'userDisplayClass': 0,
        'addressId': '',
        'deviceType': 3,
    }
    x_ = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('setHeader', 'POST',
                                                                            '/v54/ProductCategory/ListProductCategory',
                                                                            json_data, timestamp)
    headers.update(x_)
    response = requests.post('https://www.yijiupi.com/v54/ProductCategory/ListProductCategory', headers=headers,
                             json=json_data, )
    print(response.text)


# 这个是主页
getList()
# 这个是搜索页，未通过
getData()
