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


class Gessts:
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

    def ajax_requests(
            self, url: str, method: Method, headers: dict,
            cookies: dict, params: Union[dict, str, None],
            jsonData: Union[dict, None], retryTimes: int = 5,
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

    def __init_challenge(self):
        # 初始化获取验证码
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
        challenge, gt = resp['data']['geetest'].values()
        return challenge, gt

    def __get_all_info(self):
        # 这个函数是获取c，s以及坐标信息，这里的坐标是未经过处理的
        challenge, gt = self.__init_challenge()
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
        # 上述顺序不能打乱，必须严格相同
        result: dict = json.loads(pattern.findall(resp.text)[0])['data']
        pic: str = 'https://static.geetest.com' + result['pic']
        c = result['c']
        s = result['s']
        # 本地搭建了一个识别文字坐标的接口
        poses = requests.post(
            'http://127.0.0.1:8000/clickOn',
            json={
                "dataType": 1,
                "imageSource": pic
            }
        ).json()['data']['res']
        return poses, result['pic'], gt, challenge, c, s

    def do_verify(self):
        info = self.__get_all_info()
        codes, pic, gt, challenge, c, s = info
        new = []
        # 处理坐标，变为极验需要的样子
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
        # 避免出现点选过快的情况
        time.sleep(2)
        resp = self.ajax_requests(
            url='https://api.geetest.com/ajax.php',
            method='get',
            headers=self.headers,
            cookies=self.cookies,
            jsonData=None,
            params=params
        )
        print(resp.text)


if __name__ == '__main__':
    bili = Gessts()
    for _ in range(10):
        bili.do_verify()
