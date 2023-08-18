import requests
import execjs


def getSign():
    url = 'https://api.theone.art/market/api/key/get'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.theone.art',
        'Referer': 'https://www.theone.art/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    res = requests.get(url=url, headers=headers).json()
    data = str(res['data'])
    sign = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('getSign', data)
    return sign


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.theone.art',
    'Referer': 'https://www.theone.art/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sig': '8hJWPRjfS7l%2Fj86OrejRjAZDLiwIzZfQcKKIuEWB3154u4wv3WeQIv2pV3nzAo3HnXEoW0t6Tmxp9nRUjnrGtA%3D%3D',
}

for pageNum in range(1, 20):
    sign = getSign()
    hsign = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('design', sign)
    json_data = {
        'authorId': None,
        'chainContract': None,
        'commodityCategoryId': None,
        'commodityCategoryIdList': [],
        'commodityId': None,
        'highPrice': '',
        'lowPrice': '',
        'pageCount': pageNum,
        'pageSize': 20,
        'seriesWorks': None,
        'seriesWorksId': None,
        'sort': {
            'field': 2,
            'upOrDown': 1,
        },
        'statusSell': 1,
        'topicId': None,
        'typeMarket': 1,
        'commodityTraitList': [],
        'sig': sign,
    }
    response = requests.post('https://api.theone.art/market/api/saleRecord/list/v2', headers=headers,  json=json_data)
    res = response.json()["data"]
    print(res)


