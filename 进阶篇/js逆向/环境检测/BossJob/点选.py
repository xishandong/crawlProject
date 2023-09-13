import json
import re
import time
from typing import Literal, Union

import execjs
import requests

from boss.chaojiying import Chaojiying_Client

URL = [
    'https://www.zhipin.com/wapi/zpAntispam/v2/geetest/register',  # 初始化获取挑战
    'https://api.geetest.com/gettype.php',  # 初始化相关
    'https://api.geetest.com/ajax.php',  # 初始化相关
    'https://api.geetest.com/get.php',  # 获取图片
]

Method = Literal['get', 'post', 'POST', 'GET']
pattern = re.compile(r'\((.*?)\)', re.S)


class BossSlide:
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
            'randomKey': '642c15af525632c7e2c40cb2036975f5',
        }

        resp: dict = self.ajax_requests(
            url=url,
            params=params,
            method='get',
            jsonData=None,
            cookies=self.cookies,
            headers=self.headers
        ).json()
        token = ''
        _, challenge, gt = json.loads(resp['zpData']['registerResult']).values()
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
        # 这里用超级鹰
        chaojiying = Chaojiying_Client('******', '******', '96001')
        poses = chaojiying.PostPic(requests.get(pic).content, 9004)['pic_str'].split('|')
        return poses, result['pic'], gt, challenge, c, s, token

    def __do_verify(self) -> dict:
        # 极验点选验证
        info = self.__get_all_info()
        codes, pic, gt, challenge, c, s, token = info
        new = []
        # 处理坐标
        for code in codes:
            x, y = code.split(',')
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
            'randomKey': '642c15af525632c7e2c40cb2036975f5', # 随机值，和初始请求一致即可
            'seccode': validate + '|jordan'
        }

    def verify(self):
        response = requests.get(
            'https://www.zhipin.com/wapi/zpAntispam/v2/geetest/validate',
            params=self.__do_verify(),
            cookies=self.cookies,
            headers=self.headers,
        )
        print(response.text)


if __name__ == '__main__':
    print(BossSlide().verify())
