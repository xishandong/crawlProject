# 使用aiohttp中的ClientSession
import requests
import asyncio
import time
import aiohttp

urls = [
    'http://127.0.0.1:5000/dxs',
    'http://127.0.0.1:5000/dxy',
    'http://127.0.0.1:5000/date'
]


async def get_page(url):
    print('正在下载', url)
    # requests发起的请求时基于同步的，必须使用基于异步的网络请求模块进行指定url的请求发送
    # aiohttp：基于异步的网络请求
    # response = requests.get(url=url).text
    async with aiohttp.ClientSession() as session:
        # headers,params/data,proxy='http://ip:port'
        async with await session.get(url=url) as response:
            # text()返回字符串型的响应对象
            # read()返回的二进制响应对象
            # json()返回的json对象
            # 注意在获取响应数据操作之前一定要使用await进行手动挂起
            page_text = await response.text()
    print('下载完成', url)
    return page_text


def callback(task):
    print(task.result())


tasks = []

for url in urls:
    c = get_page(url)
    task = asyncio.ensure_future(c)
    task.add_done_callback(callback)
    tasks.append(task)

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()

print('总耗时', end - start)
