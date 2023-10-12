import csv
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Literal, Union, Iterator

import requests
from loguru import logger
from retrying import retry


class Log:
    log = logger

    # # 配置日志信息
    # log.add(
    #     f"log_{1}.log",  # 日子文件名，后留一个占位符
    #     rotation='1 MB',  # 日志分割，可以根据时间也可以根据大小
    #     colorize=False,  # 是否染色
    #     level='DEBUG'  # 日志等级
    # )

    @property
    def debug(self):
        return self.__class__.log.debug

    @property
    def info(self):
        return self.__class__.log.info

    @property
    def error(self):
        return self.__class__.log.error

    @property
    def exception(self):
        return self.__class__.log.exception


log = Log()


class Request_obj:
    """
    对requests的二次封装
    """
    def __init__(
            self,
            url: str,
            method: Literal['GET', 'POST', 'get', 'post'],
            headers: Union[None, dict] = None,
            params: Union[None, dict] = None,
            data: Union[None, dict] = None,
            cookies: Union[None, dict] = None,
            proxys: Union[None, dict] = None,
    ):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.cookies = cookies
        self.proxys = proxys
        self.request_args = {
            'headers': self.headers,
            'params': self.params,
            'cookies': self.cookies,
            'proxys': self.proxys
        }

    def __repr__(self):
        return f"""
                -------------- request for ----------------
                url  = {self.url}
                method = {self.method}
                args = {self.request_args}
                """


class ErrorResponse(Exception):
    """错误的返回数据"""

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.args[0]}"


class CrawlBase(object):
    """
    爬虫基类轮子，用于发送请求以及请求中间件和校验响应数据
    """
    method_processor: dict = {
        'get': requests.get,
        'post': requests.post,
    }
    session = requests.Session()
    session_method_processor: dict = {
        'get': session.get,
        'post': session.post
    }
    # 线程锁相关
    file_lock = Lock()

    @retry(
        stop_max_attempt_number=5,
        wait_exponential_multiplier=5000,
        wait_exponential_max=30000,
        retry_on_exception=lambda e: isinstance(e, (requests.RequestException, ErrorResponse))
    )
    def __ajax_requests(
            self,
            request_obj: Request_obj,
            session: bool = False
    ) -> requests.Response:
        """
        发送请求，默认重试5次，此函数是私有函数，默认无法在实例调用
        :param request_obj: 请求对象
        :param session: 是否使用session
        :return: response
        """
        if session:
            method_pro = self.session_method_processor[request_obj.method.lower()]
        else:
            method_pro = self.method_processor[request_obj.method.lower()]
        log.debug(
            f'开始发送请求 {request_obj}'
        )
        resp = method_pro(
            url=request_obj.url,
            headers=request_obj.headers,
            params=request_obj.params,
            data=json.dumps(request_obj.data, ensure_ascii=False, separators=(',', ':')).encode(),
            cookies=request_obj.cookies,
            proxies=request_obj.proxys
        )
        if not self.after_request(request_obj, resp):
            log.error(f'收到的响应数据不符合期望，抛出错误，重试...{request_obj}')
            raise ErrorResponse('用户主动抛弃当前请求')
        return resp

    def before_request(self, request_obj: Request_obj) -> None:
        """
        此函数是在发起请求前一定会访问的，可以对请求对象进行修改
        :param request_obj: 发起请求的对象
        :return:
        """
        ...

    def after_request(self, request_obj: Request_obj, response: requests.Response) -> bool:
        """
        此函数是收到响应后对响应进行校验，传入请求对象以及响应对象，如果返回false则会抛弃响应。对应返回请求体对象
        :param request_obj: 请求对象
        :param response: 响应对象
        :return:
        """
        return True

    def do_request(
            self,
            url: str,
            method: Literal['GET', 'POST', 'get', 'post'],
            headers=None,
            params=None,
            data=None,
            cookies=None,
            proxys=None,
            session: bool = False,
            middleware=None,
            is_abandon: bool = False
    ) -> Union[requests.Response, Request_obj, None]:
        """
        对requests进行二次封装，可以自定义中间件，以及是否抛弃此次请求
        :param url: url
        :param method: 方法
        :param headers: 请求头
        :param params: 请求参数
        :param data: 请求json数据
        :param cookies: cookie
        :param proxys: 代理
        :param session: 是否使用session
        :param middleware: 中间件。可接受list[func]以及func
        :param is_abandon: 是否抛弃本次请求
        :return: 错误返回None，准确返回response，抛弃返回request_obj
        """
        if proxys is None:
            proxys = {}
        if cookies is None:
            cookies = {}
        if data is None:
            data = {}
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        request_obj = Request_obj(
            url=url,
            method=method,
            headers=headers,
            params=params,
            cookies=cookies,
            proxys=proxys,
            data=data
        )
        # 执行发包前的操作
        self.before_request(request_obj)
        # 执行中间件
        if isinstance(middleware, list):
            for middle in middleware:
                middle(request_obj)
        elif middleware:
            middleware(request_obj)
        if is_abandon:
            log.debug(f'主动抛弃请求，返回请求对象...{request_obj}')
            return request_obj
        try:
            resp = self.__ajax_requests(
                request_obj=request_obj,
                session=session
            )
            return resp
        except Exception as e:
            logger.exception(e)
            return None

    def save_item_to_csv(self, items: Iterator[dict], file_path: str = 'data.csv') -> None:
        """
        批量下载数据到csv中。使用多线程下载
        :param items: 产生数据的生成器对象。需要是下载数据的dict格式
        :param file_path: 保存文件路径
        :return:
        """
        def write_items(item: dict, is_write_headers: bool):
            header = list(item.keys())
            mode = 'a' if not is_write_headers else 'w'
            with self.file_lock:
                with open(file_path, mode, encoding='utf-8', newline='') as fp:
                    writer = csv.DictWriter(fp, header)
                    if is_write_headers:
                        writer.writeheader()
                        log.info(f'写入表头了: {header}')
                    writer.writerow(item)

        is_first = True
        with ThreadPoolExecutor(max_workers=100) as executor:
            for num, save_item in enumerate(items, start=1):
                executor.submit(write_items, save_item, is_first)
                if is_first:
                    is_first = False
            log.info(f'数据写入完成, 共计{num}条数据！')
            executor.shutdown()

    # 在字典中搜索关键字，返回信息，可以搜索到字典中所有匹配的关键字
    @staticmethod
    def search_dict(items: dict, search_key: str) -> Iterator:
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
