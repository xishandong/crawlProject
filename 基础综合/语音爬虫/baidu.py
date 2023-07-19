import requests
import os
from mix_media import get


def func(text, lan):
    params = {
        'lan': lan,
        'text': text,
        'spd': '3',
        'source': 'web',
    }

    response = requests.get('https://fanyi.baidu.com/gettts', params=params)
    return response.content


def baidu(filepath, lan):
    with open(filepath, 'r', encoding='utf-8') as file:
        list = file.readlines()
    name = os.path.basename(filepath)
    if not os.path.exists(f'./media/baidu/{name}'):
        os.mkdir(f'./media/baidu/{name}')
    flag = 1
    while flag <= len(list):
        text = list[flag - 1].replace('\n', '')
        if text is not None:
            print(text)
            resp = func(text, lan)
            with open(f'./media/baidu/{name}/{flag}.mp3', 'wb') as file:
                file.write(resp)
        flag += 1
    get(f'media/baidu/{name}')
