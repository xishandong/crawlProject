import os
import requests
from lxml import html

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'cookie': '__yjs_duid=1_f064d94f3576b1069275a2e233974a2c1676030524524; PHPSESSID=1asobv9sgpl0sb0ian1dm9jcc7; sYQDUGqqzHsearch_history=%u7F8E%u5973',
    'referer': 'https://www.syt5.com/mingxing/mnmx',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}
etree = html.etree
url = 'https://www.syt5.com/mingxing/mnmx/index_%d.html'


def rebuilt_Language(url, headers):
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    return response


def getDetailInfo(url):
    all = []
    for page in range(2, 20):
        new_url = format(url % page)
        resp = rebuilt_Language(new_url, headers)
        tree = etree.HTML(resp.text)
        div_list = tree.xpath('//*[@id="body"]/main/div[4]/div/div')
        for div in div_list:
            info = {
                '标题': div.xpath('./div[1]/a/@title')[0],
                '链接': div.xpath('./div[1]/a/@href')[0]
            }
            all.append(info)
    return all


def getPhotoUrl(data):
    resp = rebuilt_Language(data['链接'], headers)
    tree = etree.HTML(resp.text)
    li_list = tree.xpath('//*[@id="showimages"]/div[3]/div[2]/div[2]/ul/li')
    url = []
    for li in li_list:
        s = li.xpath('./a/@href')[0]
        url.append(s)
    if not url:
        li_list = tree.xpath('//*[@id="showimages"]/div[3]/div[3]/div[2]/ul/li')
        for li in li_list:
            s = li.xpath('./a/@href')[0]
            url.append(s)
    info = {
        '标题': data['标题'],
        'urls': url
    }
    return info


def download(Name, url):
    resp = rebuilt_Language(url, headers)
    tree = etree.HTML(resp.text)
    src = tree.xpath('//*[@id="showpicsouutuIs2020"]/@src')[0]
    name = src.split('/')[-1]
    data = requests.get(src, headers).content
    with open(f'./{Name}/{name}', 'wb')as fp:
        fp.write(data)
    print('over!')


if __name__ == '__main__':
    total = getDetailInfo(url)
    for data in total:
        Info = getPhotoUrl(data)
        # print('正在采集'+ Info["标题"])
        # if not os.path.exists(f'./Piclib/{Info["标题"]}'):
        #     os.mkdir(f'./Piclib/{Info["标题"]}')
        # for i in range(len(Info['urls'])):
        #     download(Info['标题'],Info['urls'][i])
        print(Info)
