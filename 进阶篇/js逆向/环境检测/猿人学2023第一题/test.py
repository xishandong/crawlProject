import requests
import execjs

cookies = {
}

headers = {
    'authority': 'match2023.yuanrenxue.cn',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}
value = 0
for page in range(1, 6):
    token = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('solve', page)
    response = requests.post('https://match2023.yuanrenxue.cn/api/match2023/1', cookies=cookies, headers=headers,
                             data=token)
    data = response.json()['data']
    for v in data:
        value += v['value']
print(value)
