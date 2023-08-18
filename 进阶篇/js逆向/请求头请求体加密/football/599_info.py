import requests
import execjs
import time

headers = {
    'authority': 'api.599.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://599.com',
    'pragma': 'no-cache',
    'referer': 'https://599.com/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}
ts = int(time.time() * 1000)
pre_params = {
    "appType": "3",
    "channelNumber": "GF1001",
    "comId": "8",
    "lang": "zh",
    "platform": "pc",
    "st": ts,
    "timeZone": "8",
    "version": "671",
    "versionCode": "671"
}
sign = execjs.compile(open('js/sss.js', 'r', encoding='utf-8').read()).call('Z', '/footballapi/core/matchlist/v2/immediate', pre_params)
params = {
    'comId': '8',
    'lang': 'zh',
    'timeZone': '8',
    'version': '671',
    'versionCode': '671',
    'channelNumber': 'GF1001',
    'platform': 'pc',
    'appType': '3',
    'st': str(ts),
    'sign': sign,
}
response = requests.get('https://api.599.com/footballapi/core/matchlist/v2/immediate', params=params, headers=headers)

data = response.json()['data']
ctx = execjs.compile(open('js/demo.js', 'r', encoding='utf-8').read()).call('decrypt', data)
print(ctx)
