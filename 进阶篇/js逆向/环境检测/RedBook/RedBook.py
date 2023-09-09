import json
import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5
from urllib.parse import urlencode

import execjs
import requests

'''
已实现功能: (功能需要具有登录cookie才可以完美实现，不然会出现数据不全以及数据模糊的情况)
    1. 搜索用户，得到用户id和头像---------search_user
    2. 获取首页推荐笔记------------------get_homepage
    3. 通过用户id获取用户笔记-------------get_user_page              
    4. 通过笔记id获取笔记详情-------------get_note_detail
    5. 通过笔记id获取评论信息，带有回复的格式-get_note_comment
    6. 通过话题page_id获取话题下的笔记------search_by_topic
    7. 通过指定笔记id给笔记点赞取消点赞------like_or_dislike
    8. 指定用户id下载所有图片或者视频--------save
    9. 获取用户粉丝量----------------------get_fans
    10. 利用创作者cookie获取当前热门topic的标题，阅读量，page_id
    11. 数据库存储，用户表(uid, name, fans, note_count, liked_count)，用户话题表(id, title)，热门话题表(id, title)
    12. 搜索指定帖子
'''

URLS = [
    'https://edith.xiaohongshu.com/api/sns/web/v1/homefeed',
    'https://edith.xiaohongshu.com/api/sns/web/v1/user_posted',
    'https://edith.xiaohongshu.com/api/sns/web/v1/user_posted',
    'https://edith.xiaohongshu.com/api/sns/web/v1/search/notes',
    'https://edith.xiaohongshu.com/api/sns/web/v1/feed',
    'https://www.xiaohongshu.com/web_api/sns/v3/page/notes',
    'https://edith.xiaohongshu.com/web_api/sns/v1/search/topic',
    'https://www.xiaohongshu.com/fe_api/burdock/v2/note/',
    'https://edith.xiaohongshu.com/api/sns/web/v1/intimacy/intimacy_list/search',
    'https://www.xiaohongshu.com/user/profile/',
    'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page',
    'https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page',
    'https://edith.xiaohongshu.com/api/sns/web/v1/note/'
]


class RedBook:
    def __init__(self, cookie=None):
        self.flag = 0
        self.headers = {
            'content-type': 'application/json;charset=UTF-8',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        self.cookies = {
            'web_session': '030037a32da2185cdbc220b066234a318a6aa2',
        }
        if cookie:
            self.flag = 1
            self.cookies = cookie
        self.option = ['img_list', 'video_url']

    # 用于发送ajax请求，这里有两种情况，一种是post，一种是get
    def ajax_requests(self, url, path, params=None, json_data=None, retry_times=5):
        for _ in range(retry_times):
            try:
                if params:
                    e = path + urlencode(params)
                    ctx = self.parse_result(e)
                    self.headers['x-s'] = ctx['X-s']
                    self.headers['x-t'] = str(ctx['X-t'])
                    response = requests.get(url=url, params=params, cookies=self.cookies, headers=self.headers)
                    response.json().get('data').get('')
                    if response.json().get('success'):
                        return response.json()
                if json_data:
                    ctx = self.parse_result(path, json_data)
                    self.headers['x-s'] = ctx['X-s']
                    self.headers['x-t'] = str(ctx['X-t'])
                    response = requests.post(url=url, cookies=self.cookies, headers=self.headers,
                                             data=json.dumps(json_data, ensure_ascii=False,
                                                             separators=(',', ':')).encode())
                    response.json().get('data').get('')
                    if response.json().get('success'):
                        return response.json()
            except Exception as e:
                print(e)
                time.sleep(random.uniform(1, 5))
        return {'data': {}}

    # 获取主页推荐内容，可以不需要携带登录信息，有10种类型
    def get_homepage(self, types=0):
        category = [
            'homefeed_recommend', 'homefeed.fashion_v3', 'homefeed.food_v3', 'homefeed.cosmetics_v3',
            'homefeed.movie_and_tv_v3', 'homefeed.career_v3', 'homefeed.love_v3',
            'homefeed.household_product_v3',
            'homefeed.gaming_v3', 'homefeed.travel_v3', 'homefeed.fitness_v3'
        ]
        if types not in range(len(category)):
            raise "types only have 10 types!!"
        # 动作链
        continuations = ['']
        e = "/api/sns/web/v1/homefeed"
        url = URLS[0]
        while continuations:
            # 模拟翻页
            continuation = continuations.pop()
            json_data = {
                'cursor_score': continuation,
                'num': 36,
                'refresh_type': 1,
                'note_index': 29,
                'unread_begin_note_id': '',
                'unread_end_note_id': '',
                'unread_note_count': 0,
                'category': category[types],
            }
            # 发送请求
            resp = self.ajax_requests(url=url, path=e, json_data=json_data)
            cursor_score = resp.get('data', {}).get('cursor_score')
            # 存在下一页时执行
            if cursor_score:
                continuations.append(cursor_score)
            data = resp.get('data', {}).get('items')
            if not resp.get('success') or not data:
                break
            yield from self.get_note(data)

            time.sleep(random.uniform(1, 5))

    # 获取用户主页信息
    def get_user_page(self, user_id):
        continuations = ['']
        e = '/api/sns/web/v1/user_posted?'
        url = URLS[1]
        while continuations:
            continuation = continuations.pop()
            params = {
                'num': '30',
                'cursor': continuation,
                'user_id': user_id,
            }
            # 发送请求
            resp = self.ajax_requests(url=url, params=params, path=e)
            has_more = resp.get('data', {}).get('has_more')
            # 存在下一页就翻页
            if has_more:
                continuations.append(resp['data']['cursor'])
            data = resp.get('data', {}).get('notes')
            if data:
                yield from self.get_note(data)
            time.sleep(random.uniform(1, 5))

    def get_note_count(self, uid):
        continuations = ['']
        e = '/api/sns/web/v1/user_posted?'
        url = URLS[2]
        total = 0
        while continuations:
            continuation = continuations.pop()
            params = {
                'num': '30',
                'cursor': continuation,
                'user_id': uid,
            }
            # 发送请求
            resp = self.ajax_requests(url=url, params=params, path=e)
            has_more = resp.get('data', {}).get('has_more')
            # 存在下一页就翻页
            if has_more:
                continuations.append(resp['data']['cursor'])
            data = resp.get('data', {}).get('notes')
            total += len(data)
        return total

    # 搜索指定帖子, types：0 全部，1 视频，2 图文
    def search_notes(self, key, sorts=0, types=0):
        if sorts not in range(3) and types not in range(3):
            raise "sorts only have 3 type, and types only have 3 type..."
        # 排序 默认，最热，最新
        sort = ['general', 'popularity_descending', 'time_descending']
        page = 1
        e = '/api/sns/web/v1/search/notes'
        json_data = {
            "keyword": key,
            "page": page,
            "page_size": 20,
            "search_id": "2bpn9q2rvgfay4l6ll0m7",
            "sort": sort[sorts],
            "note_type": types,
        }
        url = URLS[3]
        continuations = [json_data]
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_requests(url=url, path=e, json_data=continuation)
            has_more = resp.get('data', {}).get('has_more')
            # 存在下一页就翻页
            if has_more:
                page += 1
                json_data['page'] = page
                continuations.append(json_data)
            data = resp.get('data', {}).get('items')
            if data:
                yield from self.get_note(data)
            time.sleep(random.uniform(1, 5))

    # 获取笔记的详细信息
    def get_note_detail(self, note_id):
        json_data = {
            'source_note_id': note_id,
        }
        url = URLS[4]
        e = '/api/sns/web/v1/feed'
        # 发送请求
        resp = self.ajax_requests(url=url, path=e, json_data=json_data)
        data = resp.get('data').get('items')
        if data:
            d = data[0]
            model_type = d.get('model_type')
            note_id = d.get('id')
            i = d.get('note_card')
            title = i.get('title')
            desc = i.get('desc')
            at_user_list = i.get('at_user_list')
            nickname = i.get('user', {}).get('nickname')
            video = i.get('video', {}).get('media', {}).get('stream', {})
            if video:
                video_url = [v.get('master_url') for v in video.get('h264', {})]
            else:
                video_url = None
            img_list = [pic.get('url') for pic in i.get('image_list', {})]
            tag_list = self.get_note_topic(note_id)
            count = i.get('interact_info')
            like_count = count.get('liked_count') if i.get('interact_info') else None
            share_count = count.get('share_count') if i.get('interact_info') else None
            collected_count = count.get('collected_count') if i.get('interact_info') else None
            comment_count = count.get('comment_count') if i.get('interact_info') else None

            item = {
                'model_type': model_type,
                'note_id': note_id,
                'title': title,
                'desc': desc,
                'user_name': nickname,
                'video_url': video_url,
                'img_list': img_list,
                'tag_list': tag_list,
                'at_user_list': at_user_list,
                'like_count': like_count,
                'share_count': share_count,
                'collected_count': collected_count,
                'comment_count': comment_count
            }

            return item

    # 获取话题下的帖子
    def search_by_topic(self, id, sort=0):
        continuations = ['']
        sorts = ['hot', 'time']
        url = URLS[5]
        e = '/web_api/sns/v3/page/notes'
        while continuations:
            continuation = continuations.pop()
            params = {
                'page_size': '20',
                'sort': sorts[sort],
                'page_id': id,
                'cursor': continuation,
                'sid': '',
            }
            resp = self.ajax_requests(url=url, path=e, params=params)
            has_more = resp.get('data', {}).get('has_more')
            # 存在下一页就翻页
            if has_more:
                continuations.append(resp['data']['cursor'])
            data = resp.get('data', {}).get('notes')
            if data:
                yield from self.get_topic_note(data)
            time.sleep(random.uniform(1, 5))

    # 搜索话题，如果接口返回为空，可以将json_data修改为注释掉的，利用前端算法获取，不走后端api
    def search_topic(self, topic: str):
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
        url = URLS[6]
        path = '/web_api/sns/v1/search/topic'
        resp = self.ajax_requests(url, path, json_data=json_data)
        data = [{
            'name': topic['name'],
            'view_num': topic['view_num'],
            'link': topic['link'],
            'id': topic['link'].split('/')[-1].split('?')[0]
        } for topic in resp['data']['topic_info_dtos']]
        data.sort(key=lambda x: x['view_num'], reverse=True)
        return data

    # 获取帖子中的tag_list，这个id是可以获取tag下的帖子的id
    def get_note_topic(self, note_id):
        url = URLS[7] + f'{note_id}/tags'
        # 标准的md5算法
        obj = md5()
        obj.update(f'/fe_api/burdock/v2/note/{note_id}/tagsWSUDD'.encode('utf-8'))
        self.headers['x-sign'] = 'X' + obj.hexdigest()
        resp = requests.get(
            url=url,
            headers=self.headers,
            cookies=self.cookies
        ).json()
        try:
            data = [{
                'name': topic['name'],
                'link': topic['link'],
                'id': topic['pageId']
            } for topic in resp['data']]
            return data
        except KeyError:
            raise KeyError(resp['msg'])

    # 搜索用户信息, 需要有cookie才可以使用
    def search_user(self, keyword):
        if self.flag:
            e = '/api/sns/web/v1/intimacy/intimacy_list/search'
            url = URLS[8]
            continuations = ['1']
            page = 1
            while continuations:
                continuation = continuations.pop()
                params = {
                    'keyword': keyword,
                    'page': continuation,
                }
                resp = self.ajax_requests(url=url, path=e, params=params)
                page += 1
                data = resp.get('data', {}).get('items')
                if data:
                    continuations.append(str(page))
                    for user in data:
                        yield user
                time.sleep(random.uniform(1, 5))
        else:
            raise TypeError("This function must have login cookie!!")

    # 获取用户粉丝量，必须在登陆后才可以获取真实数量
    def get_fans(self, uid, retry_times=3):
        for _ in range(retry_times):
            response = requests.get(URLS[9] + f'{uid}', cookies=self.cookies,
                                    headers=self.headers)
            fans = re.findall(r'上有(\d+)位粉丝', response.text)
            if fans:
                return fans
            else:
                print(f'retrying {_ + 1}/3...')
                time.sleep(random.uniform(1, 5))
        return [0]

    # 获取评论
    def get_note_comment(self, note_id):
        continuations = ['']
        e = '/api/sns/web/v2/comment/page?'
        url = URLS[10]
        # 获取不到评论结束
        while continuations:
            continuation = continuations.pop()
            params = {
                'note_id': note_id,
                'cursor': continuation,
            }
            # 发送请求
            resp = self.ajax_requests(url=url, params=params, path=e)
            has_more = resp.get('data', {}).get('has_more')
            # 存在更多评论点击更多评论
            if has_more:
                continuations.append(resp['data']['cursor'])
            data = resp.get('data', {}).get('comments')
            if data:
                yield from self.get_comment(note_id, data)
            time.sleep(random.uniform(1, 5))

    # 模拟点击更多回复
    def more_comments(self, cursor, note_id, root_id):
        continuations = [cursor]
        url = URLS[11]
        e = '/api/sns/web/v2/comment/sub/page?'
        while continuations:
            continuation = continuations.pop()
            params = {
                'note_id': note_id,
                'root_comment_id': root_id,
                'num': '10',
                'cursor': continuation,
            }
            # 发送请求
            resp = self.ajax_requests(url=url, path=e, params=params)
            has_more = resp.get('data', {}).get('has_more')
            # 若还有更多评论，则继续点击
            if has_more:
                continuations.append(resp['data']['cursor'])
            data = resp.get('data', {}).get('comments')
            if data:
                yield from self.get_comment(note_id, data)
            time.sleep(random.uniform(1, 5))

    # 获取评论信息
    def get_comment(self, note_id, comments):
        for comment in comments:
            # 如果是回复别人的评论，则会有被回复的评论的信息，没有会显示主评论
            if comment.get('target_comment', {}):
                target_comment = {
                    'id': comment.get('target_comment', {}).get('id'),
                    'user': {
                        'id': comment.get('target_comment', {}).get('user_info', {}).get('user_id'),
                        'nickname': comment.get('target_comment', {}).get('user_info', {}).get('nickname')
                    }
                }
            else:
                target_comment = "root_comment"
            content = comment['content']
            id = comment['id']
            root_id = None
            user_id = comment['user_info']['user_id']
            user_name = comment['user_info']['nickname']
            like_count = comment['like_count']
            at_users = comment.get('at_users')
            # 传递第一次的子评论
            if comment.get('sub_comments'):
                root_id = id
                yield from self.get_comment(note_id, comment['sub_comments'])
            # 模拟点击
            if comment.get('sub_comment_has_more') and root_id:
                sub_comment_cursor = comment.get('sub_comment_cursor')
                note_id = note_id
                root_comment_id = root_id
                yield from self.more_comments(sub_comment_cursor, note_id, root_comment_id)
            item = {
                'target_comment': target_comment,
                'id': id,
                'user_id': user_id,
                'user_name': user_name,
                'content': content,
                'like_count': like_count,
                'at_users': at_users
            }
            yield item

    # 获取用户某种资源的全部链接
    def get_all_url(self, uid, option):
        notes = self.get_user_page(uid)
        for note in notes:
            if self.get_note_detail(note['note_id']):
                detail = self.get_note_detail(note['note_id']).get(option)
                if detail:
                    for url in detail:
                        yield url

    # 通过uid获取图片或者视频，0为图片，1为视频
    def save(self, uid, option=0):
        if not os.path.exists('./Lib'):
            os.mkdir('./Lib')
        if option and (option != 0 and option != 1):
            raise TypeError('option must be 1 or 0!!')
        pics = self.get_all_url(uid, self.option[option])
        # 开辟线程池高效下载资源
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for pic in pics:
                future = executor.submit(self.download, pic, option)
                futures.append(future)
            for future in futures:
                future.result()
            executor.shutdown()

    # 点赞，取消点赞
    def like_or_dislike(self, note_id, option=0):
        if option and (option not in [0, 1]):
            raise TypeError("option must between integer 0 and 1 !!!")
        json_data = {
            'note_oid': note_id,
        }
        options = ['like', 'dislike']
        url = URLS[12] + f'{options[option]}'
        e = f'/api/sns/web/v1/note/{options[option]}'
        resp = self.ajax_requests(url=url, path=e, json_data=json_data)
        print(resp.get('msg'))

    # 获取用户主页的帖子和首页的帖子
    @staticmethod
    def get_note(notes):
        for note in notes:
            id = note.get('note_id')
            if note.get('hot_query'):
                # 推荐热门搜搜
                continue
            if note.get('note_card'):
                id = note.get('id')
                note = note.get('note_card')
            display_title = note.get('display_title')
            user_name = note.get('user', {}).get('nick_name')
            if not user_name:
                user_name = note.get('user', {}).get('nickname')
            user_id = note.get('user', {}).get('user_id')
            liked_count = note.get('interact_info', {}).get('liked_count')
            cover = note.get('cover', {}).get('url')
            user_cover = note.get('user', {}).get('avatar')

            item = {
                'note_id': id,
                'display_title': display_title,
                'user_name': user_name,
                'user_id': user_id,
                'liked_count': liked_count,
                'cover': cover,
                'user_cover': user_cover
            }

            yield item

    # 获取话题下的帖子
    @staticmethod
    def get_topic_note(notes):
        for note in notes:
            note_id = note.get('id')
            title = note.get('title')
            desc = note.get('desc')
            nickname = note.get('user', {}).get('nickname')
            user_id = note.get('user', {}).get('userid')
            like_count = note.get('likes')
            collected_count = note.get('collected_count')
            img_list = [pic.get('url_size_large') for pic in note.get('images_list', {})]
            video_url = note.get('video_info', {}).get('url')
            item = {
                'note_id': note_id,
                'title': title,
                'desc': desc,
                'user_id': user_id,
                'user_name': nickname,
                'video_url': video_url,
                'img_list': img_list,
                'like_count': like_count,
                'collected_count': collected_count,
            }
            yield item

    # 下载
    @staticmethod
    def download(pic, option=0, retry_times=5):
        if not os.path.exists('./Lib'):
            os.mkdir('./Lib')
        flag = ['.jpg', '.mp4']
        for _ in range(retry_times):
            try:
                path = re.sub(r'[^a-zA-Z0-9]+', '', pic.split('/')[-1])[:38] + flag[option]
                data = requests.get(pic, timeout=10)
                with open('./Lib/' + path, 'wb') as fp:
                    fp.write(data.content)
                print(pic)
                return True
            except Exception as e:
                print(f"Error:{e}, retry_times: {_ + 1}/{retry_times}...")
                time.sleep(random.uniform(1, 5))
        print(f"{pic} download Failed...")

    @staticmethod
    def parse_result(e, t=None):
        return execjs.compile(open('new/jssss.js', 'r', encoding='utf-8').read()) \
            .call('XsXt', e, t)


if __name__ == '__main__':
    cookies = {

    }
    red_book = RedBook(cookies)
    # red_book.like_or_dislike('6339534a000000001d010a74', 0)
    # items = red_book.search_user('易梦玲')
    # items = red_book.get_note_comment('6429108000000000130020d2')
    # items = red_book.get_user_page('562f8c8ef53ee026a3c94b5e')
    # items = red_book.get_homepage()
    # items = red_book.search_notes('iu')
    # items = red_book.search_topic('iu')  # 5be1b807ad586500019ce2d8
    # items = red_book.search_by_topic('5d39bbf46330d90001dc6000', 1)
    # for i in items:
    #     print(i)
    # note = red_book.get_note_detail('64a8925600000000230358af')
    # print(note)
    # topic = red_book.get_note_topic('6326a0910000000008009209')
    # print(topic)
