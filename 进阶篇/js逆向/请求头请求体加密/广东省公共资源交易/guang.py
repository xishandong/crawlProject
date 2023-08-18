import requests
import execjs

cookies = {
    '_horizon_uid': 'd6a5d5ea-b057-4431-8d41-982f8bf12b08',
    '_horizon_sid': 'e2c9e3b6-2ee8-49e6-a54a-0a15a39ee1b7',
}


def fun(page):
    json_data = {
        'type': 'trading-type',
        'publishStartTime': '',
        'publishEndTime': '',
        'siteCode': '44',
        'secondType': 'A',
        'projectType': '',
        'thirdType': '',
        'dateType': '',
        'total': 189836,
        'pageNo': page,
        'pageSize': 10,
        'openConvert': False,
    }

    data = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('hash256', json_data)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'X-Dgi-Req-App': data['App'],
        'X-Dgi-Req-Nonce': data['Nonce'],
        'X-Dgi-Req-Signature': data['Signature'],
        'X-Dgi-Req-Timestamp': str(data['Timestamp']),
    }

    response = requests.post('https://ygp.gdzwfw.gov.cn/ggzy-portal/search/v1/items', cookies=cookies, headers=headers,
                             json=json_data)
    print(response.json())


if __name__ == '__main__':
    for page in range(1, 5):
        fun(page)
