import json
import random
import re
from urllib.parse import urlparse, parse_qs

import playwright.sync_api
from playwright.sync_api import sync_playwright

# 存放滑块的页面
FILEPATH = ''

# 拦截验证的路由，自己写一下url, 格式参照playwright官网
INTERRUPT_ROUTE = ''

# 指定谷歌浏览器路径，以debug模式打开，如果已经打开了debug，下面四行代码可以注释掉
# chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
# debugging_port = "--remote-debugging-port=9999"
#
# command = f"{chrome_path} {debugging_port}"
# subprocess.Popen(command, shell=True)

# 创建的ws链接
WS_URL = 'http://localhost:your_port'


pattern = re.compile(r'\((.*)\)', re.S)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}


def get_226() -> dict:
    result: dict = {}

    def intercept_xhr(route: playwright.sync_api.Route):
        params = parse_qs(urlparse(route.request.url).query)
        result['t'] = params['t'][0]
        # 这里不指定headers会出现意想不到的错误
        resp = route.fetch(headers=headers)
        data = json.loads(pattern.findall(resp.text())[0])
        # 我们获取到了数据是不是应该返还给result
        print(data)
        route.fulfill(response=resp)

    with sync_playwright() as p:
        # 创建一个ws链接
        browser = p.chromium.connect_over_cdp(WS_URL)
        # 使用浏览器的上下文创建页面
        content = browser.contexts[0]
        page = content.new_page()
        # 设置拦截规则
        page.route(INTERRUPT_ROUTE, intercept_xhr)
        page.goto(FILEPATH)
        # 开始滑动，获取对应的东西，在滑动距离增加一些随机值
        btn = page.locator('#nc_1_n1z')
        btn_position = btn.bounding_box()
        new_x = btn_position['x'] + random.randint(290, 310)
        new_y = btn_position['y']
        page.mouse.click(btn_position['x'], btn_position['y'])
        # 滑动了
        page.mouse.down()
        page.mouse.move(new_x, new_y)
        page.mouse.up()
        # 等待一段时间以观察拖动效果
        page.wait_for_timeout(1000)
        # 关闭所有
        page.close()
        content.close()
        browser.close()
    # 返回结果
    return result
