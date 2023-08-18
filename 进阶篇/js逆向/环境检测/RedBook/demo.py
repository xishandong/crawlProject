import json
import re
from hashlib import md5
from random import uniform
from time import sleep
from typing import Union, Literal, Generator

from curl_cffi import requests

# 类型控制
Accept = Literal['json', 'text', 'contents']
Method = Literal['get', 'post']


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
            params: Union[dict, str],
            jsonData: Union[dict],
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


class NotRequiredRedBook(Base):
    def __init__(self):
        self.headers: dict = {
            'content-type': 'application/json;charset=UTF-8',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        }
        self.cookies: dict = {

        }

    # 获取话题下的帖子, 无需cookie
    def search_by_topic(self, id: Union[int, str], sort: Literal[0, 1] = 0) -> Generator:
        continuations = ['']
        sorts = ['hot', 'time']
        url = 'https://www.xiaohongshu.com/web_api/sns/v3/page/notes'
        while continuations:
            continuation = continuations.pop()
            params = {
                'page_size': '20',
                'sort': sorts[sort],
                'page_id': id,
                'cursor': continuation,
                'sid': '',
            }
            resp = self.ajax_requests(
                url=url,
                method='get',
                dataType='json',
                params=params,
                jsonData={}
            )
            has_more = resp.get('data', {}).get('has_more')
            # 存在下一页就翻页
            if has_more:
                continuations.append(resp.get('data', {}).get('cursor'))
            data = resp.get('data', {}).get('notes', {})
            yield from self.__get_topic_note__(data)
            sleep(uniform(1, 5))

    # 搜索话题, 需要有cookie才可以使用
    def search_topic(self, topic: str) -> list:
        json_data = {
            'keyword': topic,
            'suggest_topic_request': {
                'title': '',
                'desc': topic,
            },
            'page': {
                'page_size': 30,
                'page': 1,
            },
        }
        url = 'https://edith.xiaohongshu.com/web_api/sns/v1/search/topic'
        resp = self.ajax_requests(
            url=url,
            method='post',
            dataType='json',
            jsonData=json_data,
            params={}
        )
        data = [{
            'name': topic.get('name'),
            'view_num': topic.get('view_num'),
            'link': topic.get('link'),
            'id': topic.get('link', '//?').split('/')[-1].split('?')[0]
        } for topic in resp.get('data').get('topic_info_dtos', {})]
        data.sort(key=lambda x: x['view_num'], reverse=True)
        return data

    # 搜索用户信息, 需要有cookie才可以使用
    def search_user(self, keyword: str) -> Generator:
        url = 'https://edith.xiaohongshu.com/api/sns/web/v1/intimacy/intimacy_list/search'
        continuations = ['1']
        page = 1
        while continuations:
            continuation = continuations.pop()
            params = {
                'keyword': keyword,
                'page': continuation,
            }
            resp = self.ajax_requests(
                url=url,
                method='get',
                dataType='json',
                params=params,
                jsonData={}
            )
            page += 1
            data = resp.get('data', {}).get('items', [])
            if data:
                continuations.append(str(page))
            for user in data:
                yield user
            sleep(uniform(1, 5))

    # 获取帖子的tag, 需要有cookie才可以使用
    def get_note_topic(self, noteID: Union[str, int]) -> list:
        url = f'https://www.xiaohongshu.com/fe_api/burdock/v2/note/{noteID}/tags'
        # 标准的md5算法
        obj = md5()
        obj.update(f'/fe_api/burdock/v2/note/{noteID}/tagsWSUDD'.encode('utf-8'))
        self.headers['x-sign'] = 'X' + obj.hexdigest()
        resp = self.ajax_requests(
            url=url,
            method='get',
            dataType='json',
            params={},
            jsonData={}
        )
        try:
            data = [{
                'name': topic['name'],
                'link': topic['link'],
                'id': topic['pageId']
            } for topic in resp.get('data', [])]
            return data
        except KeyError:
            raise KeyError(resp['msg'])

    # 通过帖子id获取帖子信息， 无需cookie
    def get_note_by_id(self, noteID: Union[str, int]):
        url = f'https://www.xiaohongshu.com/discovery/item/{noteID}'
        resp = self.ajax_requests(
            url=url,
            method='get',
            dataType='text',
            params={},
            jsonData={}
        )
        pattern = r'<script.*?>.*?window.__INITIAL_STATE__.*?=.*?(.*?)</script>'
        noteData: dict = json.loads(re.findall(pattern, resp)[0]).get('noteData', {}).get('data')
        thisNote = noteData.get('noteData')
        relatedNotes = noteData.get('relatedNotes')
        userOtherNotesData = noteData.get('userOtherNotesData')
        return {
            'thisData': self.__get_note__(thisNote),
            'userNotesData': [self.__get_note__(n) for n in userOtherNotesData],
            'relatedNotes': [self.__get_note__(n) for n in relatedNotes]
        }

    @staticmethod
    def __get_note__(_note: dict):
        user = _note.get('user', {})
        return {
            'id': _note.get('id'),
            'title': _note.get('title'),
            'likes': _note.get('likes'),
            'collects': _note.get('collects'),
            'shareCount': _note.get('shareCount'),
            'desc': _note.get('desc'),
            'video': {
                'url': _note.get('video', {}).get('url'),
                'generatedText': _note.get('video', {}).get('generatedText'),
            },
            'imgList': [
                'https:' + img['url'] for img in _note.get('imageList', {}) if img is not None
            ],
            'time': _note.get('time'),
            'type': _note.get('type'),
            'cover': 'https:' + _note.get('cover', {}).get('url'),
            'user': {
                'id': user.get('id'),
                'gender': user.get('gender'),
                'nickname': user.get('nickname'),
                'location': user.get('location'),
                'avatar': user.get('image'),
                'desc': user.get('desc'),
                'officialVerified': user.get('officialVerified'),
                'officialVerifyName': user.get('officialVerifyName')
            }
        }

    # 获取话题下的帖子
    @staticmethod
    def __get_topic_note__(notes: dict) -> Generator:
        for note in notes:
            item = {
                'note_id': note.get('id'),
                'title': note.get('title'),
                'user_id': note.get('user', {}).get('nickname'),
                'user_name': note.get('user', {}).get('nickname'),
                'video_url': note.get('video_info', {}).get('url'),
                'img_list': [pic.get('url_size_large') for pic in note.get('images_list', {})],
                'like_count': note.get('likes'),
                'collected_count': note.get('collected_count'),
            }
            yield item


if __name__ == '__main__':
    my_book = NotRequiredRedBook()
    items = my_book.search_by_topic('5d39bbf46330d90001dc6000', 0)
    # items = my_book.search_topic('iu')
    # items = my_book.search_user('iu')
    for i in items:
        print(i)
    # topic = my_book.get_note_topic('64d22943000000000b02b559')
    # print(topic)
    # note = my_book.get_note_by_id('64d23025000000000c0370b9')
    # print(note)
