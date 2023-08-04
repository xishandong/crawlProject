import base64
import re
import time
from collections import Counter

import execjs
import requests


def remove_par(pat, string) -> (int, str):
    """
    :param pat: 需要过滤的字符
    :param string: 需要过滤的字符串
    :return: 匹配到的字符数以及过滤后的文本
    """
    pat = '{}'.format(pat)
    count = len(re.findall(pat, string))
    result = re.sub(pat, '', string)
    return count, result


def get_re_all(pat, string) -> (list, list):
    """
    :param pat: 正则表达式
    :param string: 匹配的字符串
    :return: 匹配的名字以及匹配的值
    """
    matches = re.findall(pat, string)
    variables = [match[1] for match in matches]
    variable_names = [match[0] for match in matches]
    return variables, variable_names


def get_re_search(pat, string) -> str:
    """
    :param pat: 正则表达式
    :param string: 匹配的字符串
    :return: 匹配到的结果
    """
    match = re.search(pat, string)
    if match:
        key = match.group(1)
        return key
    else:
        return ''


class weatherCrawler:
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': 'https://www.aqistudy.cn/historydata/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.cookies = {
            'Hm_lvt_6088e7f72f5a363447d4bafe03026db8': '1689668701',
            'Hm_lpvt_6088e7f72f5a363447d4bafe03026db8': str(int(time.time())),
        }
        self.city: str = ''  # 获取的城市名称
        self.file: str = '' # 动态js
        self.salt = None  # 获取md加密的盐
        self.par = None  # 获取发起post请求的data的key
        self.key_iv: list = []  # 获取动态加密用的iv
        self.key_name: list = []  # 获取动态的的密钥iv名，用于统计类型
        self.param: str = ''  # 用于发送请求的参数

    def __get_file(self):
        """
        这个函数就是获取到最终的动态js
        """
        params = {
            'city': self.city,
        }
        response = requests.get('https://www.aqistudy.cn/historydata/monthdata.php', params=params,
                                cookies=self.cookies, headers=self.headers)
        # 第一次寻找出动态js的动态链接
        match = get_re_search(r'<script[^>]*src="[^"]*\/([^\/?]+)\?t=[^"]+"', response.text)
        # 如果找到了
        if match:
            filename = 'https://www.aqistudy.cn/historydata/resource/js/' + match
            html = requests.get(filename, headers=self.headers).text
            # 执行第一次的动态js获取动态加载的参数
            pattern = r'eval\(function\(p,a,c,k,e,d\){.*?}return p}'
            _, filtered_html = remove_par(pattern, html)
            a = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read()) \
                .call('get_enc', filtered_html[1:-3])
            # 计算其中是否有eval函数，如果有则要重新运行
            count, a = remove_par('eval', a)
            if count > 0:
                # 获取执行解密base64的次数，目前观察1~2次不等
                count, a = remove_par('dweklxde', a)
                # 去除括号
                result = a.replace("(", "").replace(")", "").replace("'", '')
                # 得到完整的动态js
                self.file = self.multiple_base64_decode(result, count)
            else:
                # 没有eval说明就是完整的js
                self.file = a
        # 否则抛出错误
        else:
            raise '没有找到动态js文件'

    def __get_params(self):
        """
        这个函数是获取变化的参数，依次是变化的key和iv以及他们的名字，变化的盐，变化的请求体的键
        """
        key_iv, key_name = get_re_all(r'const\s*(\w+)\s*=\s*"([^"]+)"', self.file)
        par = get_re_search(r'data:\s*{\s*(\w+)\s*:\s*\w+\s*}', self.file)
        salt = get_re_search(r'var\s*\w+\s*=\s*\'(.*?)\'', self.file)
        self.key_name = key_name
        self.key_iv = key_iv
        self.par = par
        self.salt = salt

    def __calculate_type(self):
        """
        统计出需要加密的类型，然后得到请求体的加密参数
        """
        punctuations = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
        # 解构密钥向量的名字，用于统计
        a1_name, a2_name, a3_name, a4_name, a5_name, a6_name, a7_name, a8_name = self.key_name
        count_keys = [a3_name, a4_name, a7_name, a8_name]
        translator = str.maketrans(punctuations, ' ' * len(punctuations))
        # 统计js中密钥出现的次数来决定加密的类型
        counters = Counter(self.file.translate(translator).split())
        counts = [counters[key] for key in count_keys]
        # 下面是三种不同的类型
        if counts == [1, 1, 1, 1]:
            self.param = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read()) \
                .call('type1', self.city, self.salt)
        elif counts == [1, 1, 2, 2]:
            self.param = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read()) \
                .call('type2', self.city, self.salt, self.key_iv[6], self.key_iv[7])
        elif counts == [2, 2, 1, 1]:
            self.param = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read()) \
                .call('type3', self.city, self.salt, self.key_iv[2], self.key_iv[3])
        else:
            # 出现新的类型，查看一下，然后修改前的if条件
            print(counts)
            raise self.file

    def __do_post(self):
        """
        进行发送请求然后解密请求数据，获取到我们需要的
        """
        # 结构密钥和IV
        a1, a2, a3, a4, a5, a6, a7, a8 = self.key_iv
        data = {k: v for k, v in zip([self.par], [self.param])}
        response = requests.post('https://www.aqistudy.cn/historydata/api/historyapi.php', cookies=self.cookies,
                                 headers=self.headers,
                                 data=data)
        weather_data = execjs.compile(open('getParams.js', 'r', encoding='utf-8').read())\
            .call('decrypt', response.text, a1, a2, a5, a6)
        return weather_data['result']['data']

    def get_weather_data(self):
        """
        获取数据接口
        :return: type: dict, 天气数据
        """
        self.city = input('请输入城市名称: ')
        self.__get_file()
        self.__get_params()
        self.__calculate_type()
        return self.__do_post()

    @staticmethod
    def multiple_base64_decode(string, count) -> str:
        # 解密base64
        decoded_string = string
        for _ in range(count):
            decoded_string = base64.b64decode(decoded_string).decode("utf-8")
        return decoded_string


if __name__ == '__main__':
    obj = weatherCrawler()
    while True:
        print(obj.get_weather_data())