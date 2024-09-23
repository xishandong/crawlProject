import time

from tls_client import Session

# which need login cookie
# user info, not necessarily
# post, need
# comment, need

# cookie example
# {
#     "wd": "",
#     "dpr": "",
#     "mid": "",
#     "datr": "",
#     "ig_did": "",
#     "ig_nrcb": "",
#     "ps_l": "1",
#     "ps_n": "1",
#     "csrftoken": "",
#     "ds_user_id": "",
#     "sessionid": "",
#     "shbid": "",
#     "shbts": "",
#     "rur": ""
#     }
cookie = {
    # your cookie
}

PARAMS = r'("app_id":\s*"[^"]+")|("claim":\s*"[^"]+")|("csrf_token":\s*"[^"]+")|(["LSD",[],{"token":\s*"[^"]+")'

URLS = [
    'https://i.instagram.com/',
    'https://i.instagram.com/api/v1/users/web_profile_info/',
    'https://i.instagram.com/api/v1/feed/user',
    'https://i.instagram.com/api/v1/media/'
]
# proxy, selectable
proxy = {
    "http": "http://127.0.0.1:17890",
    "https": "http://127.0.0.1:17890",
}


class Ins:
    def __init__(self, cookies: dict):
        self.cookies = cookies
        self.session = Session(client_identifier="chrome_104", random_tls_extension_order=True)
        self.session.proxies.update(proxy)
        self.headers = {
            'sec-fetch-mode': 'cors',
            'referer': 'https://www.instagram.com/',
            'x-ig-app-id': '936619743392459',
            'sec-fetch-site': 'same-site',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'x-asbd-id': '198387',
            'accept': '*/*',
            'sec-ch-ua': 'Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'x-ig-www-claim': 'hmac.AR11qy__GsvLpiS4wKBygLGdxs2DxJB1esTkBw7b2QFaHH2d',
            'authority': 'i.instagram.com',
            'sec-ch-ua-platform': 'Windows"',
            'x-instagram-ajax': '1006400593',
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'
        }

    def ajax_request(self, url: str, /, params=None):
        """
        do requests, the engine of class
        :param url: api url
        :param params: api params
        :return: json object
        """
        for _ in range(5):
            try:
                resp = self.session.get(url, headers=self.headers, params=params, cookies=self.cookies)
                return resp.json()
            except:
                time.sleep(15)
        else:
            return None

    def get_userInfo(self, userName: str):
        """
        get user info by username
        :param userName: name of user
        :return: dict of user info
        """
        params = {
            'username': userName,
        }
        resp = self.ajax_request(URLS[1], params=params)
        if resp:
            try:
                # to avoid exception? Internet went wrong may return wrong information
                data = resp['data']['user']
            except KeyError:
                raise 'Could not get user information...'
            return {
                'biography': data.get('biography'),
                'username': data.get('username'),
                'fbid': data.get('fbid'),
                'full_name': data.get('full_name'),
                'id': data.get('id'),
                'followed_by': data.get('edge_followed_by', {}).get('count'),
                'follow': data.get('edge_follow', {}).get('count'),
                'avatar': data.get('profile_pic_url_hd'),
                'noteCount': data.get('edge_owner_to_timeline_media', {}).get('count'),
                'is_private': data.get('is_private'),
                'is_verified': data.get('is_verified')
            } if data else 'unknown User'

    def get_userPosts(self, userName: str):
        """
        get all posts from the username
        :param userName:  name
        :return: generator
        """
        continuations = [{
            'count': '12',
        }]
        temp = userName + '/username/'
        while continuations:
            continuation = continuations.pop()
            # url will change when second request and later
            url = URLS[2] + f'/{temp}'
            resp = self.ajax_request(url, params=continuation)
            # no such user
            if not resp.get('user'):
                yield 'checking cookie or unknown/private User: {}'.format(userName)
            else:
                _items = resp.get('items')
                # simulate the mousedown
                if resp.get('more_available'):
                    continuations.append({'count': '12', 'max_id': resp.get('next_max_id')})
                    user = resp.get('user')
                    temp = user.get('pk_id') if user.get('pk_id') else user.get('pk')
                yield from self.extract_post(_items)

    def get_comments(self, id):
        """
        get comments by given post id
        :param id:
        :return: generator of comments
        """
        continuations = [{
            'can_support_threading': 'true',
            'permalink_enabled': 'false',
        }]
        # base url
        url = URLS[3] + f'{id}/comments/'
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_request(url, params=continuation)
            if resp.get('next_min_id'):
                continuations.append({
                    'can_support_threading': 'true',
                    'min_id': resp.get('next_min_id')
                })
            comments = resp.get('comments')
            if comments:
                for comment in comments:
                    yield {
                        'id': comment.get('pk'),
                        'user_name': comment.get('user', {}).get('username'),
                        'user_fullname': comment.get('user', {}).get('full_name'),
                        'text': comment.get('text'),
                        'created_at': comment.get('created_at'),
                        'comment_like_count': comment.get('comment_like_count'),
                        'reply_count': comment.get('child_comment_count')
                    }
                    if comment.get('child_comment_count') > 0:
                        yield from self.get_child_comment(id, comment.get('pk'))
            else:
                yield 'no comments or losing login cookies'

    def get_child_comment(self, main_id, id):
        """
        get child of the comment by comment_id, only used in function get_comments().
        :param main_id: post id
        :param id: comment_id
        :return: to comments generator
        """
        url = f'https://www.instagram.com/api/v1/media/{main_id}/comments/{id}/child_comments/'
        continuations = [{'max_id': ''}]
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_request(url, params=continuation)
            cursor = resp.get('next_max_child_cursor')
            if cursor:
                continuations.append({'max_id': cursor})
            comments = resp.get('child_comments')
            if comments:
                for comment in comments:
                    yield {
                        'id': comment.get('pk'),
                        'user_name': comment.get('user', {}).get('username'),
                        'user_fullname': comment.get('user', {}).get('full_name'),
                        'text': comment.get('text'),
                        'created_at': comment.get('created_at'),
                        'comment_like_count': comment.get('comment_like_count'),
                    }

    @staticmethod
    def extract_post(posts):
        """
        to extract a post from a list of posts
        :param posts: original instagram posts
        :return: dict of posts
        """
        for post in posts:
            caption = post.get('caption')
            item = {
                'code': post.get('code'),
                'id': post.get('pk'),
                'pk_id': post.get('id'),
                'comment_count': post.get('comment_count'),
                'like_count': post.get('like_count'),
                'text': caption.get('text') if caption else None,
                'created_at': caption.get('created_at') if caption else post.get('taken_at'),
            }
            # other type can be added by yourself
            types = post.get('media_type')
            item.update({
                'photo': [_.get('image_versions2', {}).get('candidates', [{}])[0].get('url') for _ in
                          post.get('carousel_media')]
            }) if types == 8 else None
            item.update({
                'video': post.get('video_versions', [{}])[0].get('url')
            }) if types == 2 else None
            item.update({
                'photo': post.get('image_versions2', {}).get('candidates', [{}])[0].get('url')
            }) if types == 1 else None
            yield item


if __name__ == '__main__':
    INS = Ins(cookie)
    # items = INS.get_userPosts('renebaebae')
    items = INS.get_comments('3092771276598639274')
    for item in items:
        print(item)
        break
    item = INS.get_userInfo('renebaebae')
    print(item)
