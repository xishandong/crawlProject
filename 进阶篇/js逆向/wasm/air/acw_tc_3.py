import json
import random
import re
from urllib.parse import urlparse, parse_qs

import playwright.sync_api
import requests
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}


def replace_info(html: str):
    # 识别出requestInfo
    pattern = re.compile(r'requestInfo\s*=\s*\{.*?};', re.S)
    # 读取旧文件
    with open(FILEPATH, 'r', encoding='utf-8') as f:
        old_html = f.read()
    # 从新html中查找info, 如果有就做替换，没有就保留
    info = pattern.findall(html)[0]
    if info:
        new_html = pattern.sub(info, old_html)
        with open(FILEPATH, 'w', encoding='utf-8') as f:
            f.write(new_html)

def get_226() -> dict:
    pattern = re.compile(r'\((.*)\)', re.S)
    result: dict = {}

    def intercept_xhr(route: playwright.sync_api.Route):
        params = parse_qs(urlparse(route.request.url).query)
        result['t'] = params['t'][0]
        resp = requests.get(url=route.request.url, headers=headers)
        data = json.loads(pattern.findall(resp.text)[0])
        # 我们获取到了数据是不是应该返还给result
        print(data)
        route.abort()

    with sync_playwright() as p:
        # 使用强化脚本来过验证
        browser = p.chromium.launch(
            # headless=False,
        )
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        content = browser.new_context(user_agent=ua)
        content.add_init_script(path=r'D://crawlProjects/stealth.min.js')
        page = content.new_page()

        # # 创建一个ws链接
        # browser = p.chromium.connect_over_cdp(WS_URL)
        # # 使用浏览器的上下文创建页面
        # content = browser.contexts[0]
        # page = content.new_page()

        page.route(INTERRUPT_ROUTE, intercept_xhr)
        page.goto(FILEPATH)

        btn = page.locator('#nc_1_n1z')
        btn_position = btn.bounding_box()
        new_x = btn_position['x'] + random.randint(290, 310)
        new_y = btn_position['y']
        page.mouse.click(btn_position['x'], btn_position['y'])

        page.mouse.down()
        page.mouse.move(new_x, new_y)
        page.mouse.up()

        page.close()
        content.close()
        browser.close()

    return result

