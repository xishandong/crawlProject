import json
from random import uniform
from time import sleep
from typing import Union, Generator, Literal

from curl_cffi import requests
from ddddocr import DdddOcr
from execjs import compile

Method = Literal['get', 'post', 'POST', 'GET']


class Crawler:
    # 设置请求session
    session = requests.Session()
    # 请求方式
    methodProcessors = {
        'get': requests.get,
        'post': requests.post
    }
    sessionProcessors = {
        'get': session.get,
        'post': session.post
    }
    # 验证码识别
    ocr = DdddOcr()

    def ajax_requests(
            self, url: str,
            method: Method,
            params: dict = None,
            jsonData: dict = None,
            retryTimes: int = 10,
            timeOut: int = 20,
            headers: dict = None,
            isSession: bool = False,
            cookies: dict = None,
    ) -> requests.Response:
        methodProcessor = self.methodProcessors[method] if not isSession else self.sessionProcessors[method]
        for _ in range(retryTimes):
            try:
                response = methodProcessor(
                    url=url,
                    headers=headers,
                    cookies=cookies,
                    params=params,
                    data=json.dumps(jsonData, ensure_ascii=False, separators=(',', ':')),
                    json=jsonData,
                    timeout=timeOut
                )
                return response
            except Exception as e:
                sleep(uniform(5, 10))
                print(
                    f"错误链接: {url}",
                    f"请求出现错误, 正在重试: {_}/{retryTimes}",
                    f"错误信息为: {e}",
                    sep='\n'
                )
        else:
            raise '重试5次后仍然无法获取数据，可能是加密参数错误或者ip风控'

    def get_code(self, url: str, params: dict = None, jsonData: dict = None) -> str:
        imgBytes = self.ajax_requests(
            url=url,
            method='get',
            jsonData=jsonData,
            params=params
        ).content
        return self.ocr.classification(imgBytes)

    @staticmethod
    def open_js(path: str):
        return compile(open(path, 'r', encoding='utf-8').read())

    # 用于检查传入的键值是否正确
    @staticmethod
    def check_key(dic: dict, key: str) -> Union[str, int, list, dict]:
        if key not in dic:
            raise NameError(f'错误的初始化键值, key = {key}')
        return dic[key]

    # 在字典中搜索关键字，返回信息，可以搜索到字典中所有匹配的关键字
    @staticmethod
    def search_dict(items: dict, search_key: str) -> Generator:
        stack = [items]
        while stack:
            current_item = stack.pop()
            if isinstance(current_item, dict):
                for key, value in current_item:
                    if search_key == key:
                        yield value
                    else:
                        stack.append(value)
            elif isinstance(current_item, list):
                for value in current_item:
                    stack.append(value)
