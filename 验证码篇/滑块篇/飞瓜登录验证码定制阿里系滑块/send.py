import requests
from test import main
phone = []
for _ in phone:
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://dy.feigua.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    token = main()

    data = {
        'tel': _,
        'sessionid': token['sessionid'][0],
        'sig': token['sig'][0],
        'token': token['token'][0],
    }

    response = requests.post('https://dy.feigua.cn/login/SendLoginMessageCode', headers=headers, data=data)
    print(response.text)
