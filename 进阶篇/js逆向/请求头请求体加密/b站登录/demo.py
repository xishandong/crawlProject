import json
import re
import time
from typing import Literal, Union

import execjs
import requests

URL = [
    'https://passport.bilibili.com/x/passport-login/captcha',  # 初始化获取挑战
    'https://api.geetest.com/gettype.php',  # 初始化相关
    'https://api.geetest.com/ajax.php',  # 初始化相关
    'https://api.geetest.com/get.php',  # 获取图片
]

Method = Literal['get', 'post', 'POST', 'GET']
pattern = re.compile(r'\((.*?)\)', re.S)


class Bilibili:
    # 设置请求session
    session = requests.Session()
    # 返回指定数据类型
    dataProcessors = {
        'json': lambda resp: resp.json(),
        'text': lambda resp: resp.text,
        'contents': lambda resp: resp.content
    }
    # 请求方式
    methodProcessors = {
        'get': session.get,
        'post': session.post
    }

    def __init__(self):
        self.cookies = {
        }
        self.headers = {
            'authority': 'passport.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.bilibili.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

    def ajax_requests(
            self, url: str,
            method: Method,
            headers: dict,
            cookies: dict,
            params: Union[dict, str, None],
            jsonData: Union[dict, None],
            retryTimes: int = 5,
            timeOut: int = 20
    ) -> requests.Response:
        # 初始化请求发送器以及数据获取器

        methodProcessor = self.methodProcessors[method]
        for _ in range(retryTimes):
            try:
                return methodProcessor(
                    url=url,
                    headers=headers,
                    cookies=cookies,
                    params=params,
                    data=json.dumps(jsonData, ensure_ascii=False, separators=(',', ':')),
                    timeout=timeOut
                )
            except Exception as e:
                print(
                    f"错误链接: {url}",
                    f"请求出现错误, 正在重试: {_}/{retryTimes}",
                    f"错误信息为: {e}",
                    sep='\n'
                )
        else:
            raise '重试5次后仍然无法获取数据，可能是加密参数错误或者ip风控'

    def __init_challenge(self) -> (str, str, str):
        url = URL[0]
        params = {
            'source': 'main-fe-header',
            't': '0.26599063907171017',
        }
        resp: dict = self.ajax_requests(
            url=url,
            params=params,
            method='get',
            jsonData=None,
            cookies=self.cookies,
            headers=self.headers
        ).json()
        token = resp['data']['token']
        challenge, gt = resp['data']['geetest'].values()
        return challenge, gt, token

    def __get_all_info(self) -> (str, str, str, str, list, str, str):
        challenge, gt, token = self.__init_challenge()
        par = {
            'gt': gt,
            'callback': 'geetest_1693482668197',
        }
        self.ajax_requests(url=URL[1], headers=self.headers, cookies=self.cookies, jsonData=None, method='get',
                           params=par)
        par.update({
            'challenge': challenge,
            'lang': 'zh-cn',
            'pt': '0',
            'client_type': 'web',
            'w': '',
        })
        self.ajax_requests(url=URL[3], method='get', headers=self.headers, cookies=self.cookies, params=par,
                           jsonData=None)
        self.ajax_requests(url=URL[2], method='get', headers=self.headers, params=par, jsonData=None,
                           cookies=self.cookies)
        par.update({
            'is_next': 'true',
            'type': 'click',
            'https': 'false',
            'protocol': 'https://',
            'offline': 'false',
            'product': 'embed',
            'api_server': 'api.geetest.com',
            'isPC': 'true',
            'autoReset': 'true',
            'width': '100%',
            'callback': 'geetest_1693482668197',
        })
        resp = self.ajax_requests(url=URL[3], params=par, jsonData=None, cookies=self.cookies, headers=self.headers,
                                  method='get')
        result: dict = json.loads(pattern.findall(resp.text)[0])['data']
        pic: str = 'https://static.geetest.com' + result['pic']
        c = result['c']
        s = result['s']
        # 这里本地搭建了一个接口获取点选坐标
        poses = requests.post(
            'http://127.0.0.1:8000/clickOn',
            json={
                "dataType": 1,
                "imageSource": pic
            }
        ).json()['data']['res']
        return poses, result['pic'], gt, challenge, c, s, token

    def do_verify(self) -> dict:
        # 极验点选验证
        info = self.__get_all_info()
        codes, pic, gt, challenge, c, s, token = info
        new = []
        # 处理坐标
        for code in codes:
            x, y = (code[0] + code[2]) / 2, (code[1] + code[3]) / 2
            final_x = int(round(int(x) / 333.375 * 100 * 100, 0))
            final_y = int(round(int(y) / 333.375 * 100 * 100, 0))
            final = f'{final_x}_{final_y}'
            new.append(final)
        stringCodes = ','.join(new)
        print(
            f'处理后坐标: {stringCodes}',
            f'图片地址: {pic}',
            f'gt:{gt}, challenge:{challenge}',
            f'c: {c}, s: {s}', sep='\n'
        )
        # 加密轨迹，js代码部分可见验证码篇
        w = execjs.compile(open('main.js', 'r', encoding='utf-8').read()).call(
            'get_w',
            stringCodes, pic, gt, challenge, c, s
        )
        print(f'轨迹: {w}')
        params = {
            "gt": gt,
            "challenge": challenge,
            "lang": "zh-cn",
            "pt": "0",
            "client_type": "web",
            "w": w,
            "callback": "geetest_1694577142559"
        }
        time.sleep(2)
        resp = self.ajax_requests(
            url='https://api.geetest.com/ajax.php',
            method='get',
            headers=self.headers,
            cookies=self.cookies,
            jsonData=None,
            params=params
        )
        validate: dict = json.loads(pattern.findall(resp.text)[0])['data']['validate']
        return {
            'challenge': challenge,
            'validate': validate,
            'token': token
        }

    def do_login(self):
        user_info = {
            'user': '',
            'pwd': ''
        }
        captcha_info = self.do_verify()
        salt, public_key = self.__get_public_key()
        encrypto_pwd = self.__encrypt_pwd(user_info['pwd'], salt, public_key)
        json_data = {
            'source': 'main-fe-header',
            'username': user_info['user'],
            'password': encrypto_pwd,
            **captcha_info,
            'seccode': captcha_info['validate'] + '|jordan'
        }
        # 如果么有这两个cookie的话，登录不成功，让你用手机号登录
        self.cookies = {
            "buvid3": "DBD76116-59FE-A295-9E36-E3A5780CED3A30252infoc",
            "buvid4": "D3D33EBA-C84C-186F-6E75-726E0BF5560631645-023091314-7XDfT9HnZ77MnwndUCVxOEBHSpmaKwBBA4XcipDgJQwfLNMKNINtGA%3D%3D",
        }
        resp = requests.post('https://passport.bilibili.com/x/passport-login/web/login', cookies=self.cookies,
                             headers=self.headers, data=json_data)
        print(resp.text)
        print(resp.cookies)

    def __get_public_key(self) -> (str, str):
        # 获取密码盐以及公钥
        resp = self.ajax_requests(
            url='https://passport.bilibili.com/x/passport-login/web/key',
            method='get',
            params=None,
            jsonData=None,
            headers=self.headers,
            cookies=self.cookies
        )
        salt, public_key = resp.json()['data'].values()
        return salt, public_key

    @staticmethod
    def __encrypt_pwd(pwd: str, salt: str, public_key: str) -> str:
        # 生成加密的密码
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        import base64
        import binascii
        public_key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_v1_5.new(public_key)
        rsa_result = cipher_rsa.encrypt((salt + pwd).encode('utf-8')).hex()
        byte_data = binascii.unhexlify(rsa_result)  # 将十六进制字符串转换为字节数组
        base64_data = base64.b64encode(byte_data)  # 将字节数组转换为Base64编码
        return base64_data.decode('utf-8')


if __name__ == '__main__':
    bili = Bilibili()
    bili.do_login()
