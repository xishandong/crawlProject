import csv
import time

import requests


class Douyin:
    def __init__(self):
        self.headers = {
            'authority': 'www.douyin.com',
            'referer': 'https://www.douyin.com/',
            'sec-fetch-site': 'same-origin',
            'cookie': '',
            'pragma': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
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
            'https://www.douyin.com/aweme/v1/web/hot/search/list/'
        ]

    # 用于发送请求，设置了5次重试，一般情况如果可以获取数据5次重试就足够了
    def ajax_requests(self, position, params, retry_times=5):
        for _ in range(retry_times):
            try:
                resp = requests.get(
                    url=self.api[position], headers=self.headers, params=params, timeout=10
                ).json()
                # status_code是0的话访问就是成功的
                if not resp['status_code']:
                    return resp
            except Exception as e:
                print(e, f'retry_times:{_ + 1}:{retry_times}...')
                time.sleep(10)

    # 通过用户的加密id获取用户的信息
    # 今天这个接口1失效了，明天再试
    def get_user(self, sec_id):
        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'sec_user_id': sec_id,
        }
        # 用其他接口获取的用户信息
        data = self.ajax_requests(0, params)
        user = next(self.search_dir(data, 'author'), None)
        if user:
            return next(self.get_user_info(user), None)

    # 通过用户加密的id获取用户发布的短视频或者图文帖子相关信息
    def get_user_post(self, sec_id):
        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'channel': 'channel_pc_web',
            'sec_user_id': sec_id,
            'max_cursor': '0',
            'locate_item_id': '7220335724376182050',
            'locate_query': 'false',
            'show_live_replay_strategy': '1',
            'count': '20',
            'publish_video_strategy_type': '2',
            'pc_client_type': '1',
            'cookie_enabled': 'true',
        }
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            data = self.ajax_requests(0, continuation)
            # 模拟向下滑动
            if next(self.search_dir(data, 'has_more'), None):
                params['max_cursor'] = next(self.search_dir(data, 'max_cursor'), None)
                continuations.append(params)
            for posts in self.search_dir(data, 'aweme_list'):
                for post in posts:
                    yield from self.get_post(post)
            time.sleep(.5)

    # 通过帖子id获取帖子的全部评论
    def get_comment_by_id(self, id):
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
            data = self.ajax_requests(2, continuation)
            # 模拟向下滑动
            if next(self.search_dir(data, 'has_more'), None):
                params['cursor'] = next(self.search_dir(data, 'cursor'), None)
                continuations.append(params)
            for comment in data.get('comments'):
                yield from self.get_comment(comment)
                # 模拟点击更多回复
                if comment['reply_comment_total'] > 0:
                    more_comment_params = {
                        'aid': '6383',
                        'comment_id': comment['cid'],
                        'cursor': '0',
                        'count': '3',
                    }
                    yield from self.more_comments(more_comment_params)
                time.sleep(.5)

    # 点击更多回复触发的事件
    def more_comments(self, params):
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            data = self.ajax_requests(3, continuation)
            # 模拟点击更多回复
            if next(self.search_dir(data, 'has_more'), None):
                params['cursor'] = next(self.search_dir(data, 'cursor'), None)
                params['count'] = '10'
                continuations.append(params)
            for comment in data.get('comments'):
                yield from self.get_comment(comment)
            time.sleep(.5)

    # 通过关键词定位短视频
    # sort_type: 0为综合，1为点赞量，2为新发布
    # publish_time: 0为不限，1为一天内，7为一周内，182为半年内
    def search_key(self, key, sort_type=0, publish_time=0):
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
            data = self.ajax_requests(4, continuation)
            # 模拟向下滑动
            if next(self.search_dir(data, 'has_more'), None):
                params['offset'] = next(self.search_dir(data, 'cursor'), None)
                continuations.append(params)
            # 根据不同类型的帖子传入不同的值进行解析，如果有没见过的类型，会打印类型，用户可以自行通过类型补充在条件判断中
            for posts in self.search_dir(data, 'data'):
                for post in posts:
                    if post['type'] == 1:
                        yield from self.get_post(post['aweme_info'])
                    elif post['type'] == 16:
                        for _item in post['aweme_mix_info']['mix_items']:
                            yield from self.get_post(_item)
                    elif post['type'] == 60:
                        for items in self.search_dir(post, 'hotspot_items'):
                            for _item in items:
                                yield from self.get_post(_item)
                    elif post['type'] in [76, 77]:
                        pass
                    elif post['type'] == 4:
                        for user in post['user_list']:
                            if user.get('items'):
                                for item in user.get('items'):
                                    yield from self.get_post(item)
                    elif post['type'] == 996:
                        for items in self.search_dir(post, 'hotspot_items'):
                            for _item in items:
                                yield from self.get_post(_item)
                    else:
                        print('\n\n')
                        print(post)
                        print('\n\n')
                    time.sleep(.5)

    # 通过关键词搜索用户
    def search_user(self, key):
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
            data = self.ajax_requests(6, continuation)
            # 模拟向下滑动
            if next(self.search_dir(data, 'has_more'), None):
                params['offset'] = next(self.search_dir(data, 'cursor'), None)
                continuations.append(params)
            for user in data['user_list']:
                # 今天这个接口失效了
                yield from self.get_user_info(user.get('user_info'))
            time.sleep(.5)

    # 获取当前热搜
    def get_hotSearch(self):
        res = requests.get(self.api[7], headers=self.headers).json()
        word_list = next(self.search_dir(res, 'word_list'))
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

    # 在字典中搜索关键字，返回信息，可以搜索到字典中所有匹配的关键字
    @staticmethod
    def search_dir(items, search_key):
        stack = [items]
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
    def get_post(post):
        aweme_id = post.get('aweme_id')
        desc = post.get('desc')
        create_time = post.get('create_time')
        types = post.get('aweme_type')
        if types in [0, 55, 107]:
            source = post.get("video")['play_addr'].get('url_list')[0]
        elif types == 68:
            source = [img['url_list'][0] for img in post.get('images')]
        else:
            source = types
            print('\n\n', post, '\n\n')
        video_tag = [tag['tag_name'] for tag in post.get('video_tag')] if post.get('video_tag') else None
        text_extra = [extra.get('hashtag_name') for extra in post.get('text_extra')] if post.get('text_extra') else None
        liked = post.get('statistics').get('digg_count')
        comment_count = post.get('statistics').get('comment_count')
        share_count = post.get('statistics').get('share_count')
        collect_count = post.get('statistics').get('collect_count')
        region = post.get('region')

        yield {
            'aweme_id': aweme_id,
            'desc': desc,
            'type': 'video' if types in [0, 107, 55] else 'photo',
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
    def get_user_info(user):
        work_count = user.get('aweme_count')
        nickname = user.get("nickname")
        sec_uid = user.get('sec_uid')
        signature = user.get('signature')
        unique_id = user.get('unique_id') if user.get('unique_id') else user.get('short_id')
        total_liked = user.get('total_favorited')
        following_count = user.get('following_count')
        follower_count = user.get('follower_count')
        custom_verify = user.get('custom_verify')
        user_age = user.get('user_age')
        yield {
            'sec_uid': sec_uid,
            'unique_id': unique_id,
            'nickname': nickname,
            'custom_verify': custom_verify,
            'signature': signature,
            'work_count': work_count,
            'user_age': user_age,
            'following_count': following_count,
            'total_favorite': total_liked,
            'follower_count': follower_count
        }

    # 获取评论内容
    @staticmethod
    def get_comment(c):
        sticker = None
        cid = c.get('cid')
        create_time = c.get('create_time')
        digg_count = c.get('digg_count')
        ip_label = c.get('ip_label')
        reply_comment_total = c.get('reply_comment_total')
        text = c.get('text')
        nickname = c.get('user', {}).get('nickname')
        sec_uid = c.get('user', {}).get('sec_uid')
        reply_id = c.get('reply_id')
        reply_to_reply_id = c.get('reply_to_reply_id')
        reply_to_username = c.get('reply_to_username')
        reply_to_user_sec_id = c.get('reply_to_user_sec_id')
        if c.get('sticker'):
            if c.get('sticker').get('animate_url'):
                sticker = c.get('sticker').get('animate_url').get('url_list')[0]
            elif c.get('sticker').get('static_url'):
                sticker = c.get('sticker').get('static_url').get('url_list')[0]

        yield {
            'reply_id': reply_id,
            'comment_id': cid,
            'reply_to_reply_id': reply_to_reply_id,
            'sec_uid': sec_uid,
            'user': nickname,
            'reply_to_user_sec_id': reply_to_user_sec_id,
            'reply_to_username': reply_to_username,
            'text': text,
            'sticker': sticker,
            'liked': digg_count,
            'reply_count': reply_comment_total,
            'ip': ip_label,
            'create_time': create_time
        }

    # 下载某一个帖子内容
    def download(self, item):
        for _ in range(5):
            try:
                if item['type'] == 'photo':
                    flag = 0
                    for url in item['link']:
                        path = f'./Lib/{item["aweme_id"]}{"aa" + str(flag)}.jpg'
                        with open(path, 'wb') as fp:
                            fp.write(requests.get(url, headers=self.headers, timeout=10).content)
                        print(path)
                        flag += 1
                    return True
                else:
                    path = f'./Lib/{item["aweme_id"]}.mp4'
                    with open(path, 'wb') as fp:
                        fp.write(requests.get(item['link'], headers=self.headers, timeout=10).content)
                    print(path)
                    return True
            except Exception as e:
                print(e)
                print(item)
                time.sleep(5)

    def save2csv(self, id):
        _items = self.get_comment_by_id(id)
        header = ['reply_id', 'comment_id', 'reply_to_reply_id', 'sec_uid', 'user', 'reply_to_user_sec_id',
                  'reply_to_username', 'text', 'sticker', 'liked', 'reply_count', 'ip', 'create_time']
        fp = open(f'{id}.csv', 'w', encoding='utf-8', newline='')
        writer = csv.DictWriter(fp, header)
        writer.writeheader()
        flag = 0
        for _i in _items:
            flag += 1
            if flag % 100 == 0:
                print(f'写入{flag}条数据')
            writer.writerow(_i)


if __name__ == '__main__':
    dou = Douyin()
    # 将视频评论保存到csv中
    # dou.save2csv(7246412694926937359)
    # 获取热搜
    # items = dou.get_hotSearch()
    # 获取搜索
    # items = dou.search_key('Jennie', 2)
    # 获取用户信息
    # print(dou.get_user('MS4wLjABAAAA0fiq261i6th1gRCsGrZ6SRxCT9DdEz3aJ5nBRnR14N0'))
    # 获取用户帖子
    # items = dou.get_user_post('MS4wLjABAAAA0fiq261i6th1gRCsGrZ6SRxCT9DdEz3aJ5nBRnR14N0')
    # for item in islice(items, 1):
    #     print(item)
