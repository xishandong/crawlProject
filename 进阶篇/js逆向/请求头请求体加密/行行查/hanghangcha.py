import requests
import execjs

cookies = {
    'UM_distinctid': '185c4195bd7e6f-038d88d1a6e504-26021151-144000-185c4195bd8968',
    'Hm_lvt_1521e0fb49013136e79181f2888214a7': '1674032275',
    'Hm_lpvt_1521e0fb49013136e79181f2888214a7': '1674032275',
    'JSESSIONID': 'F83DF5ABA6CAAEE674C850D3483CB550',
    '_ACCOUNT_': 'OTM0NmEzMDU1YmEzNGY4MDk3NjliZDI4NjUyNzhmNDElNDAlNDBtb2JpbGU6MTY3NTI0MzYxNzI2NjowYjBlNmMwYzJhZTFhYjFjNzFjZjIyYTQ5MDM1ZDA4Yg',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'Auth-Plus': '',
    'Connection': 'keep-alive',
    # 'Cookie': 'UM_distinctid=185c4195bd7e6f-038d88d1a6e504-26021151-144000-185c4195bd8968; Hm_lvt_1521e0fb49013136e79181f2888214a7=1674032275; Hm_lpvt_1521e0fb49013136e79181f2888214a7=1674032275; JSESSIONID=F83DF5ABA6CAAEE674C850D3483CB550; _ACCOUNT_=OTM0NmEzMDU1YmEzNGY4MDk3NjliZDI4NjUyNzhmNDElNDAlNDBtb2JpbGU6MTY3NTI0MzYxNzI2NjowYjBlNmMwYzJhZTFhYjFjNzFjZjIyYTQ5MDM1ZDA4Yg',
    'Origin': 'https://www.hanghangcha.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'clientInfo': 'web',
    'clientVersion': '1.0.0',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'filter': '{"title":null,"sortType":null,"limit":9,"skip":0,"userId":2636778}',
}

response = requests.get(
    'https://api.hanghangcha.com/hhc/industry/articleWithTags',
    params=params,
    cookies=cookies,
    headers=headers,
)

data = response.json()['data']

ctx = str(execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('decrypt', data))

print(ctx)
