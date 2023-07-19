import asyncio
import time


async def request(url):
    print('正在下载', url)
    # 在异步协程中，如果出现了同步模块相关的代码，就无法实现异步
    # time.sleep(2)
    # 当在asyncio中遇到阻塞操作必须进行手动挂起
    await asyncio.sleep(2)
    print('下载完成', url)


urls = [
    'www.baidu.com',
    'www.douban.com',
    'www.shu.edu.cn'
]
# 任务列表：存放多个任务对象
tasks = []
for url in urls:
    c = request(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)

start = time.time()

loop = asyncio.get_event_loop()
# 需要将任务列表封装到wait中
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print(end - start)
