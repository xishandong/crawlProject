import requests
import os
from mix_media import get


def func(text, lan):
    cookies = {
        'OUTFOX_SEARCH_USER_ID_NCOO': '1065325158.1443799',
        'OUTFOX_SEARCH_USER_ID': '-527773617@180.168.188.248',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=1065325158.1443799; OUTFOX_SEARCH_USER_ID=-527773617@180.168.188.248',
        'Range': 'bytes=0-',
        'Referer': 'https://fanyi.youdao.com/',
        'Sec-Fetch-Dest': 'audio',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'audio': text,
        'le': lan,
    }

    response = requests.get('https://dict.youdao.com/dictvoice', params=params, cookies=cookies, headers=headers)
    return response.content


def youdao(filepath, lan):
    with open(filepath, 'r', encoding='utf-8') as file:
        list = file.readlines()
    name = os.path.basename(filepath)
    if not os.path.exists(f'./media/youdao/{name}'):
        os.mkdir(f'./media/youdao/{name}')
    flag = 1
    while flag <= len(list):
        text = list[flag - 1].strip()
        if text is not None:
            print(text)
            resp = func(text, lan)
            with open(f'./media/youdao/{name}/{flag}.mp3', 'wb') as file:
                file.write(resp)
        flag += 1
    get(f'media/youdao/{name}')
