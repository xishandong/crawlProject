import json
import random
import time
from itertools import islice
from typing import Generator

import requests


class Bilibili:
    cookies: dict = {
        'bili_jct': '',
        'SESSDATA': '',
    }
    headers: dict = {
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    def __init__(self):
        self.myId = '35242527'  # 个人的uid
        # 使用到的api列表
        self.apis = [
            'https://api.bilibili.com/x/msgfeed/like_detail',  # 查看点赞用户
            'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs',  # 获取私信内容
            'https://api.vc.bilibili.com/session_svr/v1/session_svr/get_sessions',  # 获取私信列表
            'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg',  # 发送私信
            'https://api.bilibili.com/x/relation/modify',  # 拉黑用户, act:5拉黑， 6取消
        ]
        # 获取的数据类型
        self.dataProcessors = {
            'json': lambda resp: resp.json(),
            'text': lambda resp: resp.text,
        }

    def ajax_get(self, *, url, params, dataType, retry_times=5):
        """
        对接口发送get请求
        :param url: 发送请求的url
        :param params: 携带的参数，在api文档中获取
        :param dataType: 想要返回的数据类型
        :param retry_times: 出现异常的重试次数
        :return: 对于的数据类型
        """
        for _ in range(retry_times):
            try:
                response = requests.get(url=url, params=params, headers=self.headers, cookies=self.cookies)
                dataProcessor = self.dataProcessors.get(dataType)
                if dataProcessor:
                    return dataProcessor(response)
                raise ValueError(f"不支持的数据类型: {dataType}")
            except requests.RequestException:
                print(f'正在重试，重试次数: {_}/{retry_times}')
                time.sleep(5)
        else:
            raise requests.RequestException('超过重试次数也无法获取数据...')

    def ajax_post(self, *, url, data, dataType, retry_times=5):
        """
        对接口发送post请求
        :param url: 发送请求的url
        :param data: 携带的参数，在api文档中获取
        :param dataType: 想要返回的数据类型
        :param retry_times: 出现异常的重试次数
        :return: 对于的数据类型
        """
        for _ in range(retry_times):
            try:
                response = requests.post(url=url, data=data, headers=self.headers, cookies=self.cookies)
                dataProcessor = self.dataProcessors.get(dataType)
                if dataProcessor:
                    return dataProcessor(response)
                raise ValueError(f"不支持的数据类型: {dataType}")
            except requests.RequestException:
                print(f'正在重试，重试次数: {_}/{retry_times}')
                time.sleep(5)
        else:
            raise requests.RequestException('超过重试次数也无法获取数据...')

    def get_like_user(self, cardId) -> Generator:
        """
        获取稿子的点赞用户信息
        :param cardId: 在消息中查看稿子对应的id，这个id在消息卡片中获取
        :return: 一个带有用户的生成器对象
        """
        page = 1
        continuations = [{
            'card_id': cardId,
            'last_view_at': '0',
            'pn': str(page),
            'build': '0',
            'mobi_app': 'web',
        }]
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_get(url=self.apis[0], params=continuation, dataType='json')
            data = resp.get('data')
            isEnd = data.get('page').get('is_end')
            if not isEnd:
                page += 1
                continuations.append({
                    'card_id': cardId,
                    'last_view_at': '0',
                    'pn': str(page),
                    'build': '0',
                    'mobi_app': 'web',
                })
            _users = data.get('items')
            yield from self.__get_user_list(_users=_users)

    def gst_chat_msg(self, mid) -> Generator:
        """
        获取和某个用户的聊天记录
        :param mid: 用户的mid
        :return: 消息记录的生成器
        """
        continuations = [{
            'sender_device_id': '1',
            'talker_id': mid,
            'session_type': '1',
            'size': '20',
            'build': '0',
            'mobi_app': 'web',
        }]
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_get(url=self.apis[1], params=continuation, dataType='json')
            messages = resp.get('data').get('messages')
            if resp.get('data').get('has_more') == 1:
                continuations.append({
                    'sender_device_id': '1',
                    'talker_id': mid,
                    'session_type': '1',
                    'size': '20',
                    'build': '0',
                    'mobi_app': 'web',
                    'end_seqno': resp.get('data').get('min_seqno')
                })
            yield from self.__get_msg(messages, mid, self.myId)

    def get_chat_list(self) -> Generator:
        """
        返回聊天列表
        :return: 聊天列表，携带有最后一条记录
        """
        continuations = [{
            'session_type': '1',
            'group_fold': '1',
            'unfollow_fold': '0',
            'sort_rule': '2',
            'build': '0',
            'mobi_app': 'web',
        }]
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_get(url=self.apis[2], params=continuation, dataType='json')
            sessionList = resp['data']['session_list']
            if resp['data']['has_more'] == 1:
                continuations.append({
                    'session_type': '1',
                    'group_fold': '1',
                    'unfollow_fold': '0',
                    'sort_rule': '2',
                    'build': '0',
                    'mobi_app': 'web',
                    'end_ts': sessionList[-1]['session_ts']
                })

            yield from self.__filter_session_list(sessionList)

    def send_msg(self, *, content, toMid) -> None:
        """
        发送私信
        :param content: 私信内容(仅纯文本)
        :param toMid: 私信对象的uid
        :return: None
        """
        senderId = self.myId
        data = {
            'msg[sender_uid]': senderId,
            'msg[receiver_id]': toMid,
            'msg[receiver_type]': '1',
            'msg[msg_type]': '1',
            'msg[msg_status]': '0',
            'msg[content]': '{"content":"%s"}' % content,
            'msg[timestamp]': str(int(time.time())),
            'msg[new_face_version]': '0',
            'msg[dev_id]': self.__generate_device_id(),
            'from_firework': '0',
            'build': '0',
            'mobi_app': 'web',
            'csrf_token': self.cookies.get('bili_jct'),
            'csrf': self.cookies.get('bili_jct'),
        }
        self.ajax_post(url=self.apis[3], data=data, dataType='json')

    def ban_or_unban_user(self, *, mid, act: int):
        """
        拉黑或取消拉黑用户
        :param mid: 用户id
        :param act: 动作，5为拉黑，6为取消拉黑
        :return: None
        """
        if act in [5, 6]:
            data = {
                'fid': mid,
                'act': str(act),
                're_src': '11',
                'spmid': '333.999.0.0',
                'csrf': self.cookies.get('bili_jct'),
            }
            self.ajax_post(url=self.apis[4], data=data, dataType='json')
            return
        raise TypeError('act仅支持5: 拉黑，6: 取消拉黑')

    def check_video_status(self, *, checkMsg, checkVideoCardId, checkNum):
        """
        检查用户是否点赞
        :param checkMsg: 触发检查的消息
        :param checkVideoCardId: 检查的稿件的点赞卡片id
        :param checkNum: 检查的私信数量
        :return: None
        """
        _chatList = islice(self.get_chat_list(), checkNum)
        likeList = self.get_like_user(cardId=checkVideoCardId)
        for _chat in _chatList:
            if _chat['last_msg'].get('content', '') == checkMsg:
                for user in likeList:
                    if _chat['mid'] == user['mid']:
                        print(f'用户 {user["nickname"]} 已点赞.')
                        break
                else:
                    self.send_msg(content='经过自动检查发现并未点赞，请及时点赞，否则系统将自动拉黑，若有异议请发送邮件',
                                  toMid=_chat['mid'])
                    # self.ban_or_unban_user(mid=_chat['mid'], act=5)

    @staticmethod
    # 获取用户信息
    def __get_user_list(_users):
        for _user in _users:
            u = _user['user']
            yield {
                'mid': u.get('mid'),
                'nickname': u.get('nickname'),
            }

    @staticmethod
    # 获取私信内容
    def __get_msg(messages, mid, me):
        sender = {
            mid: '对方发送',
            me: '自己发送'
        }
        for msg in messages:
            chatInfo = json.loads(msg.get('content'))
            if isinstance(chatInfo, dict):
                chatInfo['sender'] = sender[str(msg.get('sender_uid'))]
                yield chatInfo

    @staticmethod
    # 获取私信列表
    def __filter_session_list(session_list):
        for session in session_list:
            yield {
                'sender_uid': session['last_msg']['sender_uid'],
                'mid': session.get('talker_id'),
                'session_ts': session.get('session_ts'),
                'last_msg': json.loads(session.get('last_msg').get('content')),
            }

    @staticmethod
    # 获取一个随机的设备id
    def __generate_device_id():
        template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
        device_id = ""
        for char in template:
            if char == "x":
                device_id += random.choice("0123456789abcdef")
            elif char == "y":
                device_id += random.choice("0123456789abcdef")
            else:
                device_id += char
        return device_id.upper()
