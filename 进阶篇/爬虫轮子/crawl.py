import csv
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Literal, Union, Iterator

import requests
from loguru import logger
from prettytable import PrettyTable
from retrying import retry

COLORS = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',
    'reset': '0',
    'bright_black': '90',
    'bright_red': '91',
    'bright_green': '92',
    'bright_yellow': '93',
    'bright_blue': '94',
    'bright_magenta': '95',
    'bright_cyan': '96',
    'bright_white': '97',
}


class Log:
    log = logger

    # 配置日志信息
    def set_log_file(self, filepath: str = 'log.log', rotation: int = 10, level: str = 'DEBUG', color: bool = False):
        self.log.add(
            filepath,  # 日子文件名，后留一个占位符
            rotation=f'{rotation} MB',  # 日志分割，可以根据时间也可以根据大小
            colorize=color,  # 是否染色
            level=level  # 日志等级
        )

    def set_level(self, level):
        # 移除默认的控制台输出处理器
        self.log.remove()
        # 添加一个新的控制台输出处理器，只输出 INFO 级别或更高级别的日志消息
        logger.add(sys.stdout, level=level)

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
            'data': self.data,
            'cookies': self.cookies,
            'proxys': self.proxys
        }

    def __repr__(self):
        return f"""
                -------------- request for ----------------
                url  = {self.url}
                method = {self.method}
                args = {self.request_args}"""


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

    def __init__(self, sleep_interval: float = .5):
        self.control_sleep_time: float = sleep_interval

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
        if session:
            method_pro = self.session_method_processor[request_obj.method.lower()]
        else:
            method_pro = self.method_processor[request_obj.method.lower()]
        log.debug(
            f'开始发送请求 {request_obj}'
        )
        if request_obj.method.lower() == 'post':
            resp = method_pro(
                url=request_obj.url,
                headers=request_obj.headers,
                params=request_obj.params,
                data=json.dumps(request_obj.data, ensure_ascii=False, separators=(',', ':')).encode(),
                cookies=request_obj.cookies,
                proxies=request_obj.proxys
            )
        else:
            resp = method_pro(
                url=request_obj.url,
                headers=request_obj.headers,
                params=request_obj.params,
                cookies=request_obj.cookies,
                proxies=request_obj.proxys
            )
        if not self.after_request(request_obj, resp):
            log.error(f'收到的响应数据不符合期望，抛出错误，重试...{request_obj}')
            raise ErrorResponse('用户主动抛弃当前请求')
        return resp

    def before_request(self, request_obj: Request_obj) -> None:
        ...

    def after_request(self, request_obj: Request_obj, response: requests.Response) -> bool:
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
            is_abandon: bool = False,
    ) -> Union[requests.Response, Request_obj, None]:
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
            time.sleep(self.control_sleep_time)
            resp = self.__ajax_requests(
                request_obj=request_obj,
                session=session
            )
            return resp
        except Exception as e:
            log.exception(e)
            return None

    def save_item_to_csv(
            self,
            items: Iterator[dict],
            file_path: str = 'data.csv',
            max_workers: int = 30
    ) -> None:
        def write_items(item: dict, is_write_headers: bool):
            header = list(item.keys())
            mode = 'a' if not is_write_headers else 'w'
            with self.file_lock:
                with open(file_path, mode, encoding='utf-8', newline='') as fp:
                    writer = csv.DictWriter(fp, header)
                    if is_write_headers:
                        writer.writeheader()
                        log.info(f'写入表头了: {header}, 文件路径: {file_path}')
                    writer.writerow(item)

        is_first = True
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
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

    @staticmethod
    def format_table_print(
            items: list[dict],
            title: str = None,
            column_names: list = None, *,
            title_color: str = None,
            header_color: str = None,
            column_color: str = None,
            random_title_color: bool = False,
            random_header_color: bool = False,
            random_column_color: bool = False,
    ) -> None:
        try:
            assert items and isinstance(items, list) and isinstance(items[0], dict), ValueError(
                "items必须是列表包含字典")
        except AssertionError as e:
            log.exception(e)
            raise ValueError('0')

        # 给文字染色
        def dye_text(text: str, color: str = None, is_random: bool = False) -> str:
            keys = list(COLORS.keys())
            if is_random:
                color = random.choice(keys)
            if color in COLORS:
                return f'\033[1;{COLORS[color]}m{text}\033[0m'
            return text

        # 获取最长的键值
        max_key = [len(list(col.keys())) for col in items]
        max_key_size = max(max_key)
        # 获取key用做表格
        item_keys = list(items[max_key.index(max_key_size)].keys())
        column_list = [[] for _ in range(max_key_size)]
        for index, key in enumerate(item_keys):
            for item in items:
                column_list[index].append(item.get(key, ''))
        if not column_names:
            column_names = item_keys

        try:
            assert len(column_names) == len(item_keys), ValueError('表头长度与数据最长项不相符')
        except AssertionError as e:
            log.exception(e)
            raise ValueError('0')

        # 对表格进行一些初始化
        table = PrettyTable()
        if title:
            table.title = dye_text(title, title_color, random_title_color)

        table.add_column(dye_text('序号', header_color),
                         [dye_text(str(i), column_color, random_column_color) for i in
                          range(1, len(column_list[0]) + 1)])

        for j, column in enumerate(column_list, start=0):
            col = [dye_text(i, column_color, random_column_color) for i in column]
            table.add_column(dye_text(column_names[j], header_color, random_header_color), col)
        print(table)