import requests
import execjs


cookies = {
    'btoken': '89091VUM5EXO41RJFVJ7G478EIJV2990',
    'hy_data_2020_id': '185c2fd82a1a09-073d27a69f05c6-26021151-1327104-185c2fd82a2dcb',
    'hy_data_2020_js_sdk': '%7B%22distinct_id%22%3A%22185c2fd82a1a09-073d27a69f05c6-26021151-1327104-185c2fd82a2dcb%22%2C%22site_id%22%3A211%2C%22user_company%22%3A105%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%22185c2fd82a1a09-073d27a69f05c6-26021151-1327104-185c2fd82a2dcb%22%7D',
    'sajssdk_2020_cross_new_user': '1',
    'Hm_lvt_42317524c1662a500d12d3784dbea0f8': '1674013672',
    'Hm_lpvt_42317524c1662a500d12d3784dbea0f8': '1674021425',
}

headers = {
    'authority': 'www.xiniudata.com',
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    # 'cookie': 'btoken=89091VUM5EXO41RJFVJ7G478EIJV2990; hy_data_2020_id=185c2fd82a1a09-073d27a69f05c6-26021151-1327104-185c2fd82a2dcb; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%22185c2fd82a1a09-073d27a69f05c6-26021151-1327104-185c2fd82a2dcb%22%2C%22site_id%22%3A211%2C%22user_company%22%3A105%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%22185c2fd82a1a09-073d27a69f05c6-26021151-1327104-185c2fd82a2dcb%22%7D; sajssdk_2020_cross_new_user=1; Hm_lvt_42317524c1662a500d12d3784dbea0f8=1674013672; Hm_lpvt_42317524c1662a500d12d3784dbea0f8=1674021425',
    'origin': 'https://www.xiniudata.com',
    'referer': 'https://www.xiniudata.com/industry/newest?from=data',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

payload = {
    "sort": 1,
    "start": 0,
    "limit": 20
}

pl = str(execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('hhy', payload))
sig = str(execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('hy', payload))

json_data = {
    'payload': pl,
    'sig': sig,
    'v': 1,
}

response = requests.post(
    'https://www.xiniudata.com/api2/service/x_service/person_industry_list/list_industries_by_sort',
   # https://www.xiniudata.com/api2/service/x_service/person_industry_list/list_industries_by_sort
    cookies=cookies,
    headers=headers,
    json=json_data,
)

res = response.json()['d']

ctx = str(execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('dy', res))

print(ctx)
