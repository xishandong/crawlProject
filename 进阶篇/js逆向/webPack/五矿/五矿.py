import csv
from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from typing import TypedDict, Literal, Iterator

from crwalBase import Crawler
from encode import getParams

purchase = Literal['ZBGG', 'CQGG', 'ZGYS', 'ZBJG', 'ZBGS', 'CGGG', 'XJCQGG', 'CGJG', 'JPGG', 'JPCQ', 'JPJG']
Method = Literal['', '01', '02', '11', '12', '14', '22', '30', '0', '1']
classification = Literal['', '100', '010', '001']

URLS = [
    'https://ec.minmetals.com.cn/open/homepage/zbs/by-lx-page',
    'https://ec.minmetals.com.cn/open/homepage/cgxj/by-lx-page',
    'https://ec.minmetals.com.cn/open/homepage/jps/by-lx-page',
    'https://ec.minmetals.com.cn/open/homepage/zbs/',
    'https://ec.minmetals.com.cn/open/homepage/cgs/',
    'https://ec.minmetals.com.cn/open/homepage/jps/',
    'https://ec.minmetals.com.cn/open/homepage/public'
]


class Section(TypedDict):
    inviteMethod: Method  # 采购方式/竞价方式
    businessClassfication: classification  # 业务分类
    mc: str  # 名称
    lx: purchase  # 采购信息
    dwmc: str  # 发布公司
    pageIndex: int  # 当前页数


class Minmetals(Crawler):
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

    def announcement(self, _data: Section) -> Iterator:
        if _data['lx'] in ['ZBGG', 'CQGG', 'ZGYS', 'ZBJG', 'ZBGS']:
            url = URLS[0]
        elif _data['lx'] in ['CGGG', 'XJCQGG', 'CGJG']:
            url = URLS[1]
        else:
            url = URLS[2]
        key = self.get_public_key()
        continuations = [_data]
        while continuations:
            continuation = continuations.pop()
            par = getParams(continuation, key)
            json_data = {
                'param': par
            }
            resp: dict = self.ajax_requests(
                url=url,
                method='post',
                headers=self.headers,
                jsonData=json_data
            ).json()
            dataList: list = resp.get('list', [])

            if dataList:
                _data['pageIndex'] += 1
                continuations.append(_data)

            for notice in dataList:
                yield notice

    def save_multi(self, _data: Section, filePath: str = 'data.csv', totalPage: int = 1000):
        if _data['lx'] in ['ZBGG', 'CQGG', 'ZGYS', 'ZBJG', 'ZBGS']:
            url = URLS[0]
        elif _data['lx'] in ['CGGG', 'XJCQGG', 'CGJG']:
            url = URLS[1]
        else:
            url = URLS[2]
        key = self.get_public_key()

        def get_data_list(_url: str, page: int):
            _data['pageIndex'] = page
            par = getParams(_data, key)
            json_data = {
                'param': par
            }
            resp: dict = self.ajax_requests(
                url=url,
                method='post',
                headers=self.headers,
                jsonData=json_data
            ).json()
            dataList: list = resp.get('list', [])
            fieldnames = dataList[0].keys()
            if page == 1:
                with open(filePath, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames)
                    writer.writeheader()
            with open(filePath, mode="a", newline="", encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerows(dataList)
            print(f'写入第{page}页数据')

        get_data_list(url, 1)

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for nowPage in range(2, totalPage + 1):
                future = executor.submit(get_data_list, url, nowPage)
                futures.append(future)
            for future in futures:
                future.result()
            executor.shutdown()

    def get_details(self, id: str, lx: purchase):
        params = {'id': id}
        if lx in ['ZBGG', 'CQGG', 'ZGYS', 'ZBJG', 'ZBGS']:
            url = URLS[3] + lx.lower()
        elif lx in ['CGGG', 'XJCQGG', 'CGJG']:
            if lx == 'XJCQGG':
                lx = 'CQGG'
            url = URLS[4] + lx.lower()
        else:
            url = URLS[5] + lx.lower()
        key = self.get_public_key()
        par = getParams(params, key)
        json_data = {
            'param': par
        }
        resp: dict = self.ajax_requests(
            url=url,
            method='post',
            headers=self.headers,
            jsonData=json_data
        ).json()
        print(resp)

    def save_csv(self, _data: Section, count: int = 100, filePath: str = 'data.csv') -> None:
        dataIter: Iterator = self.announcement(_data)
        datas = list(islice(dataIter, count))
        # 写入CSV文件
        with open(filePath, mode="w", newline="", encoding='utf-8') as file:
            fieldnames = datas[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # 写入表头
            writer.writerows(datas)

        print("CSV文件写入完成。")

    def get_public_key(self) -> str:
        url = URLS[6]
        response = self.ajax_requests(
            url=url,
            method='post',
            headers=self.headers
        )
        return response.text


if __name__ == '__main__':
    mine = Minmetals()
    data: Section = {
        "inviteMethod": "",
        "businessClassfication": "",
        "mc": "",
        "lx": "ZBGG",
        "dwmc": "",
        "pageIndex": 1
    }
    mine.save_multi(data)
    # items = mine.announcement(data)
    # for item in items:
    #     print(item)
