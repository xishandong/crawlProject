import json
import re
from concurrent.futures import ThreadPoolExecutor
from csv import DictWriter
from os import path, mkdir
from random import uniform
from time import sleep
from typing import Union, Generator
from urllib.parse import urlparse, parse_qs

from 进阶篇.基础综合.weibo全站爬取.base import Base


class WeiBo(Base):
    def __init__(self, headers: dict, cookies: dict):
        self.headers.update(headers)
        self.cookies.update(cookies)
        response = self.session.get('https://m.weibo.cn/api/config', cookies=self.cookies, headers=self.headers)
        self.headers['x-xsrf-token'] = response.json()['data']['st']

    # keyword搜索
    def keyword_search(self, keyword: str) -> Generator:
        num = 1
        continuations: list = [{
            'containerid': f'100103type=1&q={keyword}',
            'page_type': 'searchall',
        }]
        while continuations:
            continuation: dict = continuations.pop()
            num += 1
            message = self.ajax_requests(
                url='https://m.weibo.cn/api/container/getIndex',
                method='get',
                dataType='json',
                params=continuation,
                jsonData=None
            )
            datas = message.get('data', {}).get('cards')
            if datas:
                continuation.update({'page': f'{num}'})
                continuations.append(continuation)
            for data in datas:
                if data.get('card_type', 0) == 9:
                    yield self.typeof_9(data)
                elif data.get('card_type', 0) == 11:
                    yield from self.typeof_11(data)
            sleep(uniform(1, 5))

    # 获取用户主页帖子
    def user_homepage(self, id: Union[int, str]) -> Generator:
        params = {
            'uid': f'{id}',
        }
        response = self.ajax_requests(
            url='https://m.weibo.cn/profile/info',
            method='get',
            dataType='json',
            params=params,
            jsonData=None,
        )
        more = response.get('data', {}).get('more', '').split('/')[-1]
        continuations = [{'containerid': more}]
        while continuations:
            continuation = continuations.pop()
            message = self.ajax_requests(
                url='https://m.weibo.cn/api/container/getIndex',
                method='get',
                dataType='json',
                params=continuation,
                jsonData=None,
            )
            if message:
                # 模拟向下滑动的操作
                info = message.get('data').get('cardlistInfo')
                continuation.update({'since_id': info.get('since_id'),
                                     'page_type': info.get('page_type')})
                continuations.append(continuation)
            datas = message.get('data').get('cards')
            for data in datas:
                if data.get('card_type', 0) == 9:
                    yield self.typeof_9(data)
                elif data.get('card_type', 0) == 11:
                    yield from self.typeof_11(data)
            sleep(uniform(1, 5))

    # 通过用户的id准确搜索用户
    def get_user_info_by_id(self, id: Union[str, int]) -> dict:
        params = {
            'uid': f'{id}',
        }
        response = self.ajax_requests(
            url='https://m.weibo.cn/profile/info',
            method='get',
            dataType='json',
            params=params,
            jsonData=None,
        )
        user = response.get('data', {}).get('user', {})
        return self.parse_user_info(user)

    # 通过用户名模糊匹配用户
    def get_user_info_by_uname(self, uname: str) -> Generator:
        num = 1
        continuations: list = [{
            'containerid': f'100103type=3&q={uname}',
            'page_type': 'searchall',
        }]
        while continuations:
            continuation: dict = continuations.pop()
            num += 1
            message = self.ajax_requests(
                url='https://m.weibo.cn/api/container/getIndex',
                method='get',
                dataType='json',
                params=continuation,
                jsonData=None
            )
            datas = message.get('data', {}).get('cards')
            if datas:
                continuation.update({'page': f'{num}'})
                continuations.append(continuation)
            for data in datas:
                if data.get('card_type', 0) == 11:
                    for card in data.get('card_group', []):
                        yield self.parse_user_info(card.get('user', {}))
            sleep(uniform(1, 5))

    # 获取用户相册图片
    def user_photo_album(self, id: Union[int, str]) -> Generator:
        def get_container_id(_url):
            return self.ajax_requests(
                url=_url,
                method='get',
                dataType='json',
                params=params,
                jsonData=None,
            )

        params = {
            'uid': f'{id}',
        }
        # 获取第一次的containerid
        response = get_container_id('https://m.weibo.cn/profile/info')
        match_obj = re.search(r'containerid=(\d+)_', response.get('data', {}).get('fans', ''))
        containerid = match_obj.group(1)
        params['containerid'] = containerid
        # 获取第二次的containerid
        response = get_container_id('https://m.weibo.cn/api/container/getIndex')
        data = response.get('data', {}).get('tabsInfo', {}).get('tabs')[-1].get('containerid')
        params['containerid'] = data
        # 获取第三次的containerid
        response = get_container_id('https://m.weibo.cn/api/container/getIndex')
        # 获取到最终需要的相册参数
        url = response.get("data", {}).get("scheme")
        url_query = urlparse(str(url)).query
        datas = parse_qs(url_query)
        params = {
            'containerid': datas.get('containerid', [])[0] + '_-_photoall',
            'count': 24,
            'title': '照片墙',
            'luicode': datas.get('luicode', [])[0],
            'lfid': datas.get('lfid', [])[0],
            'value': id
        }
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            message = self.ajax_requests(
                url='https://m.weibo.cn/api/container/getSecond',
                method='get',
                dataType='json',
                params=continuation,
                jsonData=None
            )
            data = message.get('data')
            if message.get('ok'):
                continuation.update({
                    'containerid': data.get('cardlistInfo', {}).get('containerid'),
                    'title': data.get('cardlistInfo', {}).get('title'),
                    'page': data.get('cardlistInfo', {}).get('page')
                })
                continuations.append(params)
            for pic in data.get('cards', []):
                for url in pic.get('pics', {}):
                    yield url.get('pic_mw2000')
            sleep(uniform(1, 5))

    # 保存图片至文件
    def save_user_photo(self, id: Union[int, str]) -> None:
        # 默认保存资源目录，可根据需求自行修改
        if not path.exists('./sourceLib'):
            mkdir('./sourceLib')

        # 下载
        def download_photo(_url):
            sourceType: str = _url.split('.')[-1]
            name = _url.split('/')[-1]
            if sourceType.lower() not in ['jpg', 'gif', 'png']:
                _path = f'./sourceLib/{name[0:10]}.mp4'
            else:
                _path = f'./sourceLib/{name}'
            sourceBytes = self.ajax_requests(
                url=_url,
                method='get',
                dataType='contents',
                params=None,
                jsonData=None
            )
            with open(_path, 'wb') as fp:
                fp.write(sourceBytes)
                print(_url)

        pics = self.user_photo_album(id)
        # 使用多线程下载
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            for pic in pics:
                future = executor.submit(download_photo, pic)
                futures.append(future)
            for future in futures:
                future.result()
            executor.shutdown()

    # 帖子的评论
    def post_comments(self, pid: Union[int, str]) -> Generator:
        # 解析评论
        def get_dic(_comment: dict) -> dict:
            return {
                'comment_id': _comment.get('id'),
                'user_id': _comment.get('user', {}).get('id'),
                'user_name': _comment.get('user', {}).get('screen_name'),
                'text': _comment.get('text'),
                'liked': _comment.get('like_count'),
                'location': _comment.get('source'),
                'created_at': _comment.get('created_at')
            }

        params = {
            'id': f'{pid}',
            'mid': f'{pid}',
            'max_id_type': '0',
        }
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            response = self.ajax_requests(
                url='https://m.weibo.cn/comments/hotflow',
                method='get',
                dataType='json',
                params=continuation,
                jsonData=None
            )
            data = response.get('data', {})
            # 模拟手指向下滑动
            if data.get('max_id', 0) != 0:
                continuation.update({
                    'max_id': f"{data['max_id']}",
                    'max_id_type': f'{data["max_id_type"]}',
                })
                continuations.append(continuation)
            for data in data.get('data', []):
                yield get_dic(data)
                # 获取子评，如果存在
                if data.get('comments'):
                    for comment in data.get('comments'):
                        yield get_dic(comment)
            sleep(uniform(1, 5))

    # 保存评论内容至csv
    def save_comments_to_csv(self, pid: Union[int, str]) -> None:
        comments = self.post_comments(pid)
        header = ['comment_id', 'user_id', 'user_name', 'text', 'liked', 'location', 'created_at']
        fp = open(f'{pid}.csv', 'w', encoding='utf-8', newline='')
        writer = DictWriter(fp, header)
        writer.writeheader()
        num = 0
        for comment in comments:
            writer.writerow(comment)
            num += 1
            if num % 100 == 0:
                print(f'写入{num}条数据')

    def post_info(self, pid: Union[int, str]) -> dict:
        url = f'https://m.weibo.cn/detail/{pid}'
        response = self.ajax_requests(
            url=url,
            method='get',
            dataType='text',
            params=None,
            jsonData=None
        )
        render_data = re.findall(r'<script>.*?render_data\s*=\s*\[({.*?})].*?</script>', response.replace('\n', ''))[0]
        return self.typeof_9({'mblog': json.loads(render_data).get('status', {})})

    # 获取模式为11下的帖子
    def typeof_11(self, mblog: dict) -> Generator:
        cards = mblog.get('card_group', [])
        for card in cards:
            if card.get('card_type') == 9:
                yield self.typeof_9(card)

    # 获取模式为9下面的文章
    @staticmethod
    def typeof_9(mblog: dict) -> dict:
        mlog = mblog.get('mblog', {})
        mid = mlog.get('mid') if mlog.get('mid') else mlog.get('id')
        regionName = mlog.get('region_name')
        createdAt = mlog.get('created_at')
        text = mlog.get('text')
        author = mlog.get('user', {}).get('screen_name')
        pageInfo = mlog.get('page_info')
        commentCount = mlog.get('comments_count')
        likeCount = mlog.get('attitudes_count')
        info = {
            'cover': pageInfo.get('page_pic', {}).get('url'),
            'page_url': pageInfo.get('page_url'),
            'description': pageInfo.get('content1'),
            'page_title': pageInfo.get('page_title'),
            'type': pageInfo.get('type'),
        } if pageInfo else None
        pic = [d.get('url') for d in mlog.get('pics', []) if d.get('url')]
        video = [d.get('videoSrc') for d in mlog.get('pics', []) if d.get('videoSrc')]

        return {
            'created_at': createdAt,
            'mid': mid,
            'region_name': regionName,
            'text': text,
            'like_count': likeCount,
            'comments_count': commentCount,
            'author': author,
            'pic': pic,
            'video': video,
            'page_info': info
        }

    @staticmethod
    def parse_user_info(user: dict) -> dict:
        return {
            'id': user.get('id'),
            'username': user.get('screen_name'),
            'avatar': user.get('avatar_hd'),
            'description': user.get('description'),
            'profile_url': user.get('profile_url'),
            'cover_image': user.get('cover_image_phone'),
            'verified': user.get('verified'),
            'verified_reason': user.get('verified_reason'),
            'follow_count': user.get('follow_count'),
            'followers_count': user.get('followers_count'),
            'gender': user.get('gender')
        }


if __name__ == '__main__':
    headers = {}
    cookies = {}
    weibo = WeiBo(headers=headers, cookies=cookies)
    # 用户相册
    # items = w.user_photo_album('7690783385')
    # 帖子评论
    # items = w.post_comments(4931686942905084)
    # 模糊搜索用户
    # items = weibo.get_user_info_by_uname('iu')
    # 帖子搜索
    # items = weibo.keyword_search('iu')
    # for i in items:
    #     print(i)

    # 保存评论
    # weibo.save_comments_to_csv(4931686942905084)
    # 保存相片
    # weibo.save_user_photo('7690783385')

    # 帖子详情
    # print(weibo.post_info(4931686942905084))
    # 精确搜索用户
    # print(weibo.get_user_info_by_id('7690783385'))
