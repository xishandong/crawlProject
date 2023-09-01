import requests
import execjs

anti_content = execjs.compile(open('hello.js', 'r', encoding='utf-8').read()).call('dt')

headers = {
    'Accept': 'application/json, text/javascript',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

params = {
    'tf_id': 'TFRQ0v00000Y_13394',
    'page': '1',
    'size': '100',
    'anti_content': anti_content
}

response = requests.get('https://apiv2.pinduoduo.com/api/gindex/tf/query_tf_goods_info', params=params, headers=headers)
print(response.text)
