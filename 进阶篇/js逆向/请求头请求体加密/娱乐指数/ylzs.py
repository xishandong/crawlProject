import requests
import execjs

cookies = {
    'mobile_iindex_uuid': '9f0ae384-2821-5797-8a76-87bb1cef4a1f',
    'Hm_lvt_2873e2b0bdd5404c734992cd3ae7253f': '1674101222,1674103567',
    'Hm_lpvt_2873e2b0bdd5404c734992cd3ae7253f': '1674103567',
}

headers = {
    'authority': 'www.chinaindex.net',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    # 'cookie': 'mobile_iindex_uuid=9f0ae384-2821-5797-8a76-87bb1cef4a1f; Hm_lvt_2873e2b0bdd5404c734992cd3ae7253f=1674101222,1674103567; Hm_lpvt_2873e2b0bdd5404c734992cd3ae7253f=1674103567',
    'funcid': 'undefined',
    'incognitomode': '0',
    'referer': 'https://www.chinaindex.net/ranklist/5/0',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'uuid': '9f0ae384-2821-5797-8a76-87bb1cef4a1f',
}

params = {
    'keyWord': '李知恩',
    'sign': 'b3776cdf6331ee0f6653d1de544291c3'
}

response = requests.get(
    'https://www.chinaindex.net/iIndexMobileServer/mobile/comm/getSearchResult',
    params=params,
    cookies=cookies,
    headers=headers,
)

r = response.json()['data']
lastFetchTime = response.json()['lastFetchTime']

ctx = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('decrypt', r, lastFetchTime)

print(ctx)