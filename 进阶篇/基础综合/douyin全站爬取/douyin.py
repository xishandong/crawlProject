import csv
import json
import os
import time
from threading import Lock, Condition
from concurrent.futures import ThreadPoolExecutor
from typing import Union
from urllib.parse import urlencode

import execjs
import requests
from loguru import logger
from retrying import retry


class Douyin:
    def __init__(self):
        self.headers = {
            'authority': 'www.douyin.com',
            'referer': 'https://www.douyin.com/',
            'sec-fetch-site': 'same-origin',
            'pragma': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        self.cookies = {
            "sid_tt": "585fa50b2957def5b8679dda6e5afbc7",
        }
        # 访问所需的api接口
        self.api = [
            'https://www.douyin.com/aweme/v1/web/aweme/post/',
            'https://www.douyin.com/aweme/v1/web/user/profile/other/',
            'https://www.douyin.com/aweme/v1/web/comment/list/',
            'https://www.douyin.com/aweme/v1/web/comment/list/reply/',
            'https://www.douyin.com/aweme/v1/web/general/search/single/',
            'https://www.douyin.com/aweme/v1/web/hot/search/list/',
            'https://www.douyin.com/aweme/v1/web/discover/search/',
        ]
        # 线程锁相关
        self.write_in_progress = False
        self.file_lock = Lock()
        self.write_condition = Condition(lock=self.file_lock)

    # 用于发送请求，设置了5次重试，一般情况如果可以获取数据5次重试就足够了
    @retry(stop_max_attempt_number=5, wait_exponential_multiplier=1000, wait_exponential_max=20000)
    def ajax_requests(self, position, params):
        url = self.api[position]
        full_url = urlencode(params)
        # 找到一个可以生成x-b的代码即可
        xb = execjs.compile(open('x-b.js', 'r', encoding='utf-8').read()).call('sign', full_url,
                                                                               self.headers['user-agent'])
        params['X-Bogus'] = xb
        logger.debug(f'开始发送{url}请求, 携带的参数为: {params}')
        resp = requests.get(
            url=url, headers=self.headers, params=params, timeout=10, cookies=self.cookies
        ).json()
        del params['X-Bogus']
        if not resp['status_code']:
            return resp
        return {}

    # 通过用户的加密id获取用户的信息
    def get_user(self, sec_id):
        logger.debug(f"开始请求用户信息, {sec_id}")
        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'sec_user_id': sec_id,
        }
        # 用其他接口获取的用户信息
        try:
            data = self.ajax_requests(1, params)
        except json.JSONDecodeError:
            logger.error(
                f'超过五次服务器未返回信息，更新cookie或者检查加密参数是否错误，发送错误api编号{1}, params: {params}')
            return None
        user = next(self.__search_dir(data, 'user'), None)
        if user:
            logger.info('获取到用户信息')
            return next(self.__get_user_info(user), None)
        return None

    # 通过用户加密的id获取用户发布的短视频或者图文帖子相关信息
    def get_user_post(self, sec_id):
        logger.debug(f'开始请求用户帖子: {sec_id}')
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "sec_user_id": sec_id,
            "max_cursor": "0",
            "count": "20",
        }
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            try:
                data = self.ajax_requests(0, continuation)
            except json.JSONDecodeError:
                logger.error(
                    f'超过五次服务器未返回信息，更新cookie或者检查加密参数是否错误，发送错误api编号{0}, params: {continuation}')
                return None
            # 模拟向下滑动
            if next(self.__search_dir(data, 'has_more'), None):
                params['max_cursor'] = str(next(self.__search_dir(data, 'max_cursor'), None))
                continuations.append(params)
            for posts in self.__search_dir(data, 'aweme_list'):
                for post in posts:
                    yield from self.__get_post(post)
                    self.__sleep_time(1)
            self.__sleep_time()

    # 通过帖子id获取帖子的全部评论
    def get_comment_by_id(self, id):
        logger.debug(f"开始请求用户评论, 帖子id: {id}")
        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'aweme_id': id,
            'cursor': '0',
            'count': '20',
        }
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            try:
                data = self.ajax_requests(2, continuation)
            except json.JSONDecodeError:
                logger.error(
                    f'超过五次服务器未返回信息，更新cookie或者检查加密参数是否错误，发送错误api编号{2}, params: {continuation}')
                return None
            # 模拟向下滑动
            if next(self.__search_dir(data, 'has_more'), None):
                params['cursor'] = next(self.__search_dir(data, 'cursor'), None)
                continuations.append(params)
            if not data.get('comments'):
                logger.info(f'帖子:{id}, 么有评论哦~')
                return None
            for comment in data.get('comments'):
                yield from self.__get_comment(comment)
                # 模拟点击更多回复
                if comment['reply_comment_total'] > 0:
                    more_comment_params = {
                        'aid': '6383',
                        'comment_id': comment['cid'],
                        'cursor': '0',
                        'count': '10',
                    }
                    yield from self.more_comments(more_comment_params)
            self.__sleep_time()

    # 点击更多回复触发的事件
    def more_comments(self, params):
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            try:
                data = self.ajax_requests(3, continuation)
            except json.JSONDecodeError:
                logger.error(
                    f'超过五次服务器未返回信息，更新cookie或者检查加密参数是否错误，发送错误api编号{3}, params: {continuation}')
                return None
            # 模拟点击更多回复
            if next(self.__search_dir(data, 'has_more'), None):
                params['cursor'] = next(self.__search_dir(data, 'cursor'), None)
                params['count'] = '10'
                continuations.append(params)
            for comment in data.get('comments'):
                yield from self.__get_comment(comment)

    # 通过关键词定位短视频
    # sort_type: 0为综合，1为点赞量，2为新发布
    # publish_time: 0为不限，1为一天内，7为一周内，182为半年内
    def search_key(self, key, sort_type=0, publish_time=0):
        assert sort_type in [0, 1, 2], '排序仅支持0, 1, 2'
        assert publish_time in [0, 1, 7, 182], '发行时间仅支持0, 1, 7, 182'
        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'keyword': key,
            'sort_type': str(sort_type),
            'publish_time': str(publish_time),
            'search_source': 'normal_search',
            'query_correct_type': '1',
            'is_filter_search': '0',
            'from_group_id': '',
            'offset': '0',
            'count': '15',
        }
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            try:
                data = self.ajax_requests(4, continuation)
            except json.JSONDecodeError:
                logger.error(
                    f'超过五次服务器未返回信息，更新cookie或者检查加密参数是否错误，发送错误api编号{4}, params: {continuation}')
                return None
            # 模拟向下滑动
            if next(self.__search_dir(data, 'has_more'), None):
                params['offset'] = next(self.__search_dir(data, 'cursor'), None)
                continuations.append(params)
            # 根据不同类型的帖子传入不同的值进行解析，如果有没见过的类型，会打印类型，用户可以自行通过类型补充在条件判断中
            for posts in self.__search_dir(data, 'data'):
                for post in posts:
                    if post['type'] == 1:
                        yield from self.__get_post(post['aweme_info'])
                    elif post['type'] == 16:
                        for _item in post['aweme_mix_info']['mix_items']:
                            yield from self.__get_post(_item)
                    elif post['type'] == 60:
                        for items in self.__search_dir(post, 'hotspot_items'):
                            for _item in items:
                                yield from self.__get_post(_item)
                    elif post['type'] in [76, 77]:
                        pass
                    elif post['type'] == 4:
                        for user in post['user_list']:
                            if user.get('items'):
                                for item in user.get('items'):
                                    yield from self.__get_post(item)
                    elif post['type'] == 996:
                        for items in self.__search_dir(post, 'hotspot_items'):
                            for _item in items:
                                yield from self.__get_post(_item)
                    else:
                        logger.error(f'出现未知帖子类型(搜索页): {post}')
            self.__sleep_time()

    # 通过关键词搜索用户
    def search_user(self, key):
        logger.debug(f"开始搜索用户: {key}")
        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'keyword': key,
            'search_source': 'normal_search',
            'search_channel': 'aweme_user_web',
            'offset': '0',
            'count': '10',
        }
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            try:
                data = self.ajax_requests(6, continuation)
            except json.JSONDecodeError:
                logger.error(
                    f'超过五次服务器未返回信息，更新cookie或者检查加密参数是否错误，发送错误api编号{6}, params: {continuation}')
                return None
            # 模拟向下滑动
            if next(self.__search_dir(data, 'has_more'), None):
                params['offset'] = next(self.__search_dir(data, 'cursor'), None)
                continuations.append(params)
            for user in data['user_list']:
                yield from self.__get_user_info(user.get('user_info'))
            self.__sleep_time()

    # 获取当前热搜
    def get_hotSearch(self):
        logger.debug("开始搜索热搜")
        try:
            res = self.ajax_requests(5, params={})
        except json.JSONDecodeError:
            logger.error(
                f'超过五次服务器未返回信息，更新cookie或者检查加密参数是否错误，发送错误api编号{5}')
            return None
        word_list = next(self.__search_dir(res, 'word_list'))
        # 只爬取了热搜，如果想要其他信息可以自行找api接口
        for hotpoint in word_list:
            word = hotpoint.get('word')
            hot_value = hotpoint.get('hot_value')
            event_time = hotpoint.get('event_time')

            yield {
                'word': word,
                'hot_value': hot_value,
                'event_time': event_time
            }

    def save_comment_to_csv_by_id(self, id):
        def write_comments(is_write_headers, comment=None):
            header = ['reply_id', 'comment_id', 'reply_to_reply_id', 'sec_uid', 'user', 'reply_to_user_sec_id',
                      'reply_to_username', 'text', 'sticker', 'liked', 'reply_count', 'ip', 'create_time']
            mode = 'a' if not is_write_headers else 'w'
            with self.file_lock:
                with open(f'{id}.csv', mode, encoding='utf-8', newline='') as fp:
                    writer = csv.DictWriter(fp, header)
                    if is_write_headers:
                        writer.writeheader()
                        logger.debug('写入表头了')
                    if comment:
                        writer.writerow(comment)

            with self.file_lock:
                # 等待写入权限
                while self.write_in_progress:
                    self.write_condition.wait()
                # 占位
                self.write_in_progress = True
                with open(f'{id}.csv', mode, encoding='utf-8', newline='') as fp:
                    writer = csv.DictWriter(fp, header)
                    if is_write_headers:
                        writer.writeheader()
                    if comment:
                        writer.writerow(comment)
                # 完成写入，释放写入权限
                self.write_in_progress = False
                self.write_condition.notify_all()

        _items = self.get_comment_by_id(id)

        is_first = True
        # 使用多线程下载
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            for _i in _items:
                if is_first and _i:
                    write_comments(is_first)
                    is_first = False
                future = executor.submit(write_comments, is_first, _i)
                futures.append(future)
            for future in futures:
                future.result()
            executor.shutdown()
        logger.info(f'帖子: {id}下载完毕...')

    def download_user_all_posts(self, user_id):
        user: dict = self.get_user(user_id)
        assert user is not None, "获取用户失败!请检查用户id"
        logger.info(f'获取用户成功, 用户名: {user["nickname"]}, {user}')
        folder_path = './users/' + user['unique_id']
        # 创建用户文件夹
        os.makedirs(folder_path, exist_ok=True)
        with open(folder_path + '/user_info.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(user, ensure_ascii=False))
        logger.info(f'下载用户: {user["nickname"]}信息完成')
        # 创建图片文件夹
        os.makedirs(folder_path + '/img', exist_ok=True)
        # 创建视频文件夹
        os.makedirs(folder_path + '/video', exist_ok=True)
        posts = self.get_user_post(user_id)
        assert posts is not None, '用户未发布帖子'
        # 使用多线程下载
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = []
            for post in posts:
                future = executor.submit(self.__download, post, folder_path)
                futures.append(future)
            for future in futures:
                future.result()
            executor.shutdown()

    def __download(self, _item, folder_path='./Lib'):
        @retry(stop_max_attempt_number=7, wait_exponential_multiplier=1000, wait_exponential_max=20000)
        def download_source(link, path):
            with open(path, 'wb') as fp:
                fp.write(requests.get(link, headers=self.headers, timeout=10).content)

        logger.info(f'====={_item["desc"]}, 开始下载!=====')
        if _item['type'] == 'photo':
            flag = 0
            for url in _item['link']:
                path = f'{folder_path}/img/{_item["aweme_id"]}{"aa" + str(flag)}.jpg'
                try:
                    download_source(url, path)
                except requests.RequestException:
                    logger.error(f'下载资源: {url}错误，超过五次，请手动重试. -->{_item}')
                    continue
                flag += 1
            logger.info(f'*****{_item["desc"]}, 下载完成!*****')
            return True
        else:
            path = f'{folder_path}/video/{_item["aweme_id"]}.mp4'
            try:
                download_source(_item['link'], path)
            except requests.RequestException:
                logger.error(f'下载资源: {_item["link"]}错误，超过五次，请手动重试. --> {_item}')
                return False
            logger.info(f'*****{_item["desc"]}, 下载完成!*****')
            return True

    # 在字典中搜索关键字，返回信息，可以搜索到字典中所有匹配的关键字
    @staticmethod
    def __search_dir(_items, search_key):
        stack = [_items]
        while stack:
            current_item = stack.pop()
            if isinstance(current_item, dict):
                for key, value in current_item.items():
                    if key == search_key:
                        yield value
                    else:
                        stack.append(value)
            if isinstance(current_item, list):
                for value in current_item:
                    stack.append(value)

    # 获取帖子的内容
    @staticmethod
    def __get_post(post):
        aweme_id = post.get('aweme_id')
        desc = post.get('desc')
        create_time = post.get('create_time')
        types = post.get('aweme_type')

        video_types = [0, 55, 61, 107, 51, 53]

        if types in video_types:
            source = post.get("video")['play_addr'].get('url_list')[0]
        elif types == 68:
            source = [img['url_list'][0] for img in post.get('images')]
        elif types == 101:
            return
        else:
            logger.error(f'出现未知帖子类型: {post}')
            return
        video_tag = [tag['tag_name'] for tag in post.get('video_tag')] if post.get('video_tag') else None
        text_extra = [extra.get('hashtag_name') for extra in post.get('text_extra')] if post.get(
            'text_extra') else None
        liked = post.get('statistics', {}).get('digg_count')
        comment_count = post.get('statistics', {}).get('comment_count')
        share_count = post.get('statistics', {}).get('share_count')
        collect_count = post.get('statistics', {}).get('collect_count')
        region = post.get('region')

        yield {
            'aweme_id': aweme_id,
            'desc': desc,
            'type': 'video' if types in video_types else 'photo',
            'create_time': create_time,
            'link': source,
            'video_tag': video_tag,
            'text_extra': text_extra,
            'region': region,
            'liked': liked,
            'comment_count': comment_count,
            'collect_count': collect_count,
            'share_count': share_count
        }

    # 获取用户信息
    @staticmethod
    def __get_user_info(user):
        city = str(user.get('city'))
        country = str(user.get('country'))
        district = str(user.get('district'))
        province = str(user.get('province'))
        yield {
            'sec_uid': user.get('sec_uid'),
            'unique_id': user.get('unique_id') if user.get('unique_id') else user.get('short_id'),
            'nickname': user.get("nickname"),
            'custom_verify': user.get('custom_verify'),
            'signature': user.get('signature'),
            'work_count': user.get('aweme_count'),
            'user_age': user.get('user_age'),
            'following_count': user.get('following_count'),
            'total_favorite': user.get('total_favorited'),
            'follower_count': user.get('follower_count'),
            'location': '|'.join([district, city, province, country]),
            'ip_location': user.get('ip_location'),
            'school': user.get('school_name', '暂无')
        }

    # 获取评论内容
    @staticmethod
    def __get_comment(c):
        sticker = None
        if c.get('sticker'):
            if c.get('sticker').get('animate_url'):
                sticker = c.get('sticker').get('animate_url').get('url_list')[0]
            elif c.get('sticker').get('static_url'):
                sticker = c.get('sticker').get('static_url').get('url_list')[0]
        yield {
            'reply_id': c.get('reply_id'),
            'comment_id': c.get('cid'),
            'reply_to_reply_id': c.get('reply_to_reply_id'),
            'sec_uid': c.get('user', {}).get('sec_uid'),
            'user': c.get('user', {}).get('nickname'),
            'reply_to_user_sec_id': c.get('reply_to_user_sec_id'),
            'reply_to_username': c.get('reply_to_username'),
            'text': c.get('text'),
            'sticker': sticker,
            'liked': c.get('digg_count'),
            'reply_count': c.get('reply_comment_total'),
            'ip': c.get('ip_label'),
            'create_time': c.get('create_time')
        }

    @staticmethod
    def __sleep_time(t: Union[int, float] = 1.5):
        time.sleep(t)


if __name__ == '__main__':
    dou = Douyin()
    # 保存帖子评论
    dou.save_comment_to_csv_by_id('7260706141649390904')
    # 获取帖子评论
    # items = dou.get_comment_by_id('7260706141649390904')
    # 获取热搜
    # items = dou.get_hotSearch()
    # 关键词搜索
    # items = dou.search_key('Jennie', 0)
    # 搜索用户
    # items = dou.search_user('26478510937')
    # 获取用户信息
    # print(dou.get_user('MS4wLjABAAAA9IWeOQVdHpQwC-apWrvw1QV3Gw0BZjARF7K9MenAK4TPEpk06olW1enFCFyDiE0c'))
    # 保存用户所有帖子，分门别类，视频和图片以及个人信息
    # dou.download_user_all_posts('MS4wLjABAAAAyJa3vYALkXuCuyrV9PLRHdUMgMQVXqUM-ZOkFkgO30pf-CzpwEhYR3CMDWPB1MKH')
    # 获取用户帖子
    # items = dou.get_user_post('MS4wLjABAAAA0fiq261i6th1gRCsGrZ6SRxCT9DdEz3aJ5nBRnR14N0')

    # for item in items:
    #     print(item)
