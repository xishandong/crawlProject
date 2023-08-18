import asyncio
import aiofile
import requests
from lxml import html
import os
import aiohttp

etree = html.etree
cookies = {
    'Hm_lvt_c8263f264e5db13b29b03baeb1840f60': '1676030483',
    'Hm_lpvt_c8263f264e5db13b29b03baeb1840f60': '1676030939',
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_c8263f264e5db13b29b03baeb1840f60=1676030483; Hm_lpvt_c8263f264e5db13b29b03baeb1840f60=1676030939',
    'Referer': 'https://www.3gbizhi.com/tag/meinv/2.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def getUrl(page):
    all = []
    response = requests.get(f'https://desk.3gbizhi.com/deskMV/index_{page}.html', cookies=cookies, headers=headers)
    tree = etree.HTML(response.text)
    li_list = tree.xpath('/html/body/div[5]/ul/li')
    for li in li_list:
        photo = {
            '标题': li.xpath('./a/img/@title')[0],
            'url': li.xpath('./a/@href')[0]
        }
        all.append(photo)
    return all


def getpic(data):
    response = requests.get(data['url'], headers, cookies=cookies).text
    tree = etree.HTML(response)
    url = tree.xpath('//*[@id="showimg"]/a[4]/img/@src')[0]
    return url


async def thread(url, name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False, headers=headers, cookies=cookies) as resp:
            datas = await resp.read()
            async with aiofile.async_open(f'./picLibs/{name}.jpg', 'wb') as fp:
                await fp.write(datas)
                print(name + '爬取成功!')


if __name__ == '__main__':
    if not os.path.exists('./picLibs'):
        os.mkdir('./picLibs')
    loop = asyncio.get_event_loop()
    for page in range(1, 24):
        print(page)
        all = getUrl(page)
        URL = []
        for data in all:
            url = getpic(data)
            name = data['标题']
            URL.append(thread(url, name))
        loop.run_until_complete(asyncio.wait(URL))
    loop.close()

