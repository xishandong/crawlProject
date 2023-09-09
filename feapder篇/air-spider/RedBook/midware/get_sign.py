from hashlib import md5
from urllib.parse import urlparse, urlencode


def add_sign(request):
    url = request.url
    parsed_url = urlparse(url)
    path = parsed_url.path
    params = request.params
    if params:
        path += '?' + urlencode(params)
    obj = md5()
    obj.update(f'{path}WSUDD'.encode('utf-8'))
    request.headers = {
        'x-sign': 'X' + obj.hexdigest()
    }

    return request
