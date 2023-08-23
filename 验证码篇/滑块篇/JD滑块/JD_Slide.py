import base64
import json
import re
import time
from typing import Literal, Union, Tuple

import ddddocr
import execjs
import requests

Method = Literal['get', 'post']

URLS = [
    'https://iv.jd.com/slide/g.html',
    'https://iv.jd.com/slide/s.html'
]


class JD_Slide:
    # 请求方式
    methodProcessors = {
        'get': requests.get,
        'post': requests.post
    }
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    cookies: dict = {
        # 此参数可以从浏览器中获取，固定
        '3AB9D23F7A4B3C9B': ''
    }

    def ajax_request(
            self,
            url: str,
            method: Method,
            params: Union[dict, None] = None,
            jsonData: Union[dict, None] = None,
            retryTimes: int = 5,
            timeout: int = 10
    ) -> requests.Response:
        methodProcessor = self.methodProcessors[method]
        for _ in range(retryTimes):
            try:
                response = methodProcessor(
                    url=url,
                    params=params,
                    data=json.dumps(jsonData, ensure_ascii=False, separators=(',', ':')),
                    timeout=timeout,
                    headers=self.headers,
                    cookies=self.cookies
                )
                return response
            except requests.RequestException as e:
                print(
                    f'出现错误: {e}',
                    f'错误链接: {url}',
                    f'正在重试: {_}/{retryTimes}',
                    sep='\n'
                )
        else:
            raise f'经过{retryTimes}次尝试仍然无法获取数据'

    def get_slide(self) -> Tuple[str, int]:

        def recognize_captcha(bg: bytes, patch: bytes):
            ocr = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
            return ocr.slide_match(background_bytes=bg, target_bytes=patch, simple_target=True)

        params = {
            'appId': '1604ebb2287',
            'scene': 'login',
            'product': 'click-bind-suspend',
            'e': self.cookies['3AB9D23F7A4B3C9B'],
            'j': '',
            'lang': 'zh_CN',
            'callback': 'jsonp_07985243061196063',
        }
        resp = self.ajax_request(
            url=URLS[0],
            params=params,
            jsonData=None,
            method='get'
        )
        pattern = re.compile(r'\((.*)\)', re.S)
        picData: dict = json.loads(pattern.findall(resp.text)[0])
        challenge: str = picData['challenge']
        baseBG: str = picData['bg']
        basePatch: str = picData['patch']
        byteBG: bytes = base64.b64decode(baseBG)
        bytePatch: bytes = base64.b64decode(basePatch)
        result: dict = recognize_captcha(byteBG, bytePatch)
        distance: int = round(result.get('target', [])[0] * 278 / 360 + 23)
        return challenge, distance

    def do_slide(self):
        challenge, distance = self.get_slide()
        print(challenge, distance)
        time.sleep(5)
        trace = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('generate_trace', distance)
        params = {
            'd': trace,
            'c': challenge,
            'w': '278',
            'appId': '1604ebb2287',
            'scene': 'login',
            'product': 'click-bind-suspend',
            'e': self.cookies['3AB9D23F7A4B3C9B'],
            'j': '',
            's': '3694159118904001942',
            'o': '123456',
            'o1': '0',
            'u': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcountry%3DUSA',
            'lang': 'zh_CN',
            'callback': 'jsonp_07985243061196063',
        }
        resp = self.ajax_request(
            url=URLS[1],
            params=params,
            jsonData=None,
            method='get'
        )
        print(resp.text)


if __name__ == '__main__':
    jd = JD_Slide()
    for _ in range(10):
        jd.do_slide()
