import json
import time

import execjs
from curl_cffi import requests

URLS = [
    'https://www.yijiupi.com/v54/ProductCategory/ListCategoryTree',
    'https://www.yijiupi.com/v54/PurchaseChannel/List',
    'https://www.yijiupi.com/v54/ProductCategory/ListProductCategory'
]


def get_data(json_data, url, sepUrl):
    timestamp = str(int(time.time()))
    headers = {
        'Content-Type': 'application/json',
        'token': '',
    }
    # 问题的关键是把中文好好处理!!
    data = json.dumps(json_data, ensure_ascii=False, separators=(',', ':'))
    x_ = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()) \
        .call('setHeader', 'POST', sepUrl, data, timestamp)
    headers.update(x_)
    response = requests.post(url, headers=headers,
                             data=data, impersonate='chrome110')
    print(response.json())


if __name__ == '__main__':
    set1 = {
        'json_data': {
            'data': {
                'zoneId': '4932265882383941446',
            },
            'cityId': '701',
            'userClassId': 1,
            'userDisplayClass': 0,
            'addressId': '',
            'deviceType': 3,
        },
        'url': URLS[0],
        'sepUrl': '/v54/ProductCategory/ListCategoryTree'
    }
    # get_data(**set1)
    set2 = {
        'json_data': {
            'cityId': '701',
            'userClassId': 1,
            'userDisplayClass': 0,
            'addressId': '',
            'deviceType': 3,
        },
        'url': URLS[1],
        'sepUrl': '/v54/PurchaseChannel/List'
    }
    # get_data(**set2)
    set3 = {
        'json_data': {
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
        },
        'url': URLS[2],
        'sepUrl': '/v54/ProductCategory/ListProductCategory'
    }
    get_data(**set3)
