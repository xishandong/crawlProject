import base64
import re
import time
from collections import Counter

import execjs
import requests


def remove_par(pat, string) -> (int, str):
    pat = '{}'.format(pat)
    count = len(re.findall(pat, string))
    result = re.sub(pat, '', string)
    return count, result


def multiple_base64_decode(string, count) -> str:
    decoded_string = string
    for _ in range(count):
        decoded_string = base64.b64decode(decoded_string).decode("utf-8")
    return decoded_string


def get_re_all(pat, string) -> (list, list):
    matches = re.findall(pat, string)
    variables = [match[1] for match in matches]
    variable_names = [match[0] for match in matches]
    return variables, variable_names


def get_re_search(pat, string) -> str:
    match = re.search(pat, string)
    if match:
        key = match.group(1)
        return key
    else:
        return ''


def get_file(city):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'https://www.aqistudy.cn/historydata/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    cookies = {
        'Hm_lvt_6088e7f72f5a363447d4bafe03026db8': '1689668701',
        'Hm_lpvt_6088e7f72f5a363447d4bafe03026db8': str(int(time.time())),
    }
    params = {
        'city': city,
    }
    response = requests.get('https://www.aqistudy.cn/historydata/monthdata.php', params=params, cookies=cookies,
                            headers=headers)
    match = get_re_search(r'<script[^>]*src="[^"]*\/([^\/?]+)\?t=[^"]+"', response.text)
    if match:
        filename = 'https://www.aqistudy.cn/historydata/resource/js/' + match
        html = requests.get(filename, headers=headers).text
        pattern = r'eval\(function\(p,a,c,k,e,d\){.*?}return p}'
        _, filtered_html = remove_par(pattern, html)
        a = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read()).call('get_enc', filtered_html[1:-3])
        count, a = remove_par('eval', a)
        if count > 0:
            count, a = remove_par('dweklxde', a)
            result = a.replace("(", "").replace(")", "").replace("'", '')
            data = multiple_base64_decode(result, count)
            return data
        else:
            return a
    return None


def get_params(data):
    key_iv, key_name = get_re_all(r'const\s*(\w+)\s*=\s*"([^"]+)"', data)
    par = get_re_search(r'data:\s*{\s*(\w+)\s*:\s*\w+\s*}', data)
    salt = get_re_search(r'var\s*\w+\s*=\s*\'(.*?)\'', data)
    return (key_name, key_iv), par, salt


def calculate_type(string, keys: list):
    '''
    :param string: 得到的动态js
    :param keys: 需要统计的密钥次数
    :return: 返回加密参数的类型
    '''
    punctuations = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
    translator = str.maketrans(punctuations, ' ' * len(punctuations))
    counters = Counter(string.translate(translator).split())
    counts = [counters[key] for key in keys]
    print(counts)
    # 全为1说明参数加密只有base
    if counts == [1, 1, 1, 1]:
        return 1
    elif counts == [1, 1, 2, 2]:
        return 2
    elif counts == [2, 2, 1, 1]:
        return 3
    print(string)


def do_post(par_key, value, decrypto_dict):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'https://www.aqistudy.cn/historydata/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    cookies = {
        'Hm_lvt_6088e7f72f5a363447d4bafe03026db8': '1689668701',
        'Hm_lpvt_6088e7f72f5a363447d4bafe03026db8': str(int(time.time())),
    }
    data = {k: v for k, v in zip([par_key], [value])}
    response = requests.post('https://www.aqistudy.cn/historydata/api/historyapi.php', cookies=cookies, headers=headers,
                             data=data)
    decrypto_dict['data'] = response.text
    weather_data = execjs.compile(
        open('getParams.js', 'r', encoding='utf-8').read()).call(
        'decrypt', decrypto_dict['data'], decrypto_dict['a1'], decrypto_dict['a2'],
        decrypto_dict['a5'], decrypto_dict['a6']
    )
    print(weather_data['result']['data'])


if __name__ == '__main__':
    citys = ['泸州', '上海', '北京', '杭州', '重庆']
    for city in citys:
        file = get_file(city)
        datas = get_params(file)
        a1_name, a2_name, a3_name, a4_name, a5_name, a6_name, a7_name, a8_name = datas[0][0]
        a1, a2, a3, a4, a5, a6, a7, a8 = datas[0][1]
        par_key = datas[1]
        salt = datas[2]
        calculate_key = [a3_name, a4_name, a7_name, a8_name]
        types = calculate_type(file, calculate_key)
        decrypto_dict = {
            'a1': a1,
            'a2': a2,
            'a5': a5,
            'a6': a6
        }
        print(salt)
        if types == 1:
            value = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read()).call('type1', city, salt)
            do_post(par_key, value, decrypto_dict)
        elif types == 2:
            value = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read()).call('type2', city, salt, a7, a8)
            do_post(par_key, value, decrypto_dict)
        elif types == 3:
            value = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read()).call('type3', city, salt, a3, a4)
            do_post(par_key, value, decrypto_dict)
