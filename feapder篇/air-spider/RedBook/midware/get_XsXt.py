import json
import os
from urllib.parse import urlparse, urlencode

import execjs


def get_XsXt(api: str, payload: dict = None) -> dict:
    # 获取RedBook/midware/jsCode/jsss.js的绝对路径
    js_path: str = os.path.abspath(os.path.dirname(__file__) + '/jsCode/jsss.js')
    js = execjs.compile(open(js_path, 'r', encoding='utf-8').read())
    # 加密参数
    ctx: dict = js.call('XsXt', api, payload)
    return {
        'x-s': ctx['X-s'],
        'x-t': str(ctx['X-t']),
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
    }


def add_XsXt(request):
    url = request.url
    parsed_url = urlparse(url)
    path = parsed_url.path
    method = request.method

    if method == 'GET':
        # GET请求需要拼接params和url
        params = request.params
        path = path + '?' + urlencode(params)
        request.headers = get_XsXt(path)
    elif method == 'POST':
        # POST请求需要加密payload
        json_data = request.json
        request.data = json.dumps(json_data, ensure_ascii=False,
                                  separators=(',', ':')).encode()
        request.headers = get_XsXt(path, json_data)
    return request
