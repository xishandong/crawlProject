import json
from Crypto.Cipher import AES
import base64
import time
from hashlib import md5
import requests


def sign():
    t = int(time.time() * 1000)
    n = f'client=fanyideskweb&mysticTime={t}&product=webfanyi&key=fsdsogkndfokasodnaso'
    obj = md5()
    obj.update(n.encode('utf-8'))
    sign = obj.hexdigest()
    return sign


def decrypto(data):
    key = b'\x08\x14\x9d\xa7\x3c\x59\xce\x62\x55\x5b\x01\xe9\x2f\x34\xe8\x38'
    iv = b'\xd2\xbb\x1b\xfd\xe8\x3b\x38\xc3\x44\x36\x63\x57\xb7\x9c\xae\x1c'
    aes = AES.new(key, AES.MODE_CBC, iv)
    den_text = aes.decrypt(base64.urlsafe_b64decode(data))
    return str(den_text, 'utf-8').strip()


def post(w, f, t):
    cookies = {
        'OUTFOX_SEARCH_USER_ID': '123456789@192.168.60.5',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=340028215.7799288; OUTFOX_SEARCH_USER_ID=-1551186736@49.52.96.107; P_INFO=18608219667|1670406132|1|youdaonote|00&99|null&null&null#shh&null#10#0|&0||18608219667',
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'i': w,
        'from': f,
        'to': t,
        'dictResult': 'true',
        'keyid': 'webfanyi',
        'sign': sign(),
        'client': 'fanyideskweb',
        'product': 'webfanyi',
        'appVersion': '1.0.0',
        'vendor': 'web',
        'pointParam': 'client,mysticTime,product',
        'mysticTime': str(int(time.time() * 1000)),
        'keyfrom': 'fanyi.web',
    }
    response = requests.post('https://dict.youdao.com/webtranslate', headers=headers, data=data, cookies=cookies)
    return response.text


if __name__ == '__main__':
    while True:
        try:
            From = input('请输入开始语言(自动auto, 中文zh-CHS, 韩文ko, 英文en)\n')
            To = input('请输入翻译的语言(默认, 中文zh-CHS, 韩文ko, 英文en)\n')
            word = input('请输入单词:')
            enc = post(word, From, To)
            ctx = decrypto(enc)
            print(ctx)
        except:
            print('出现异常，请重新输入!')
            continue
