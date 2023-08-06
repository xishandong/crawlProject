import json
from random import uniform
from time import sleep
from typing import Union, Literal

from curl_cffi import requests

# 类型控制
Accept = Literal['json', 'text', 'contents']
Method = Literal['get', 'post', 'POST', 'GET']


class Base:
    # 设置请求session
    session = requests.Session()
    # 请求头
    headers: dict = {}
    # 用户cookie
    cookies: dict = {}
    # 返回指定数据类型
    dataProcessors = {
        'json': lambda resp: resp.json(),
        'text': lambda resp: resp.text,
        'contents': lambda resp: resp.content
    }
    # 请求方式
    methodProcessors = {
        'get': requests.get,
        'post': requests.post
    }

    def ajax_requests(
            self, url: str,
            method: Method,
            dataType: Accept,
            params: Union[dict, str, None],
            jsonData: Union[dict, None],
            retryTimes: int = 5,
            timeOut: int = 20
    ) -> Union[dict, str, bytes]:
        # 初始化请求发送器以及数据获取器
        dataProcessor = self.dataProcessors[dataType]
        methodProcessor = self.methodProcessors[method]
        for _ in range(retryTimes):
            try:
                response = methodProcessor(
                    url=url,
                    headers=self.headers,
                    cookies=self.cookies,
                    params=params,
                    data=json.dumps(jsonData, ensure_ascii=False, separators=(',', ':')),
                    timeout=timeOut
                )
                return dataProcessor(response)
            except json.decoder.JSONDecodeError:
                raise ValueError(f'无法被解析为json格式，错误链接为: {url}')
            except Exception as e:
                sleep(uniform(1, 5))
                print(
                    f"错误链接: {url}",
                    f"请求出现错误, 正在重试: {_}/{retryTimes}",
                    f"错误信息为: {e}",
                    sep='\n'
                )
        else:
            raise '重试5次后仍然无法获取数据，可能是加密参数错误或者ip风控'
