import subprocess

import playwright.sync_api
from playwright.sync_api import sync_playwright

# 存放滑块的页面
FILEPATH = ''


def acw_tc_v() -> dict:
    # 指定谷歌浏览器路径，以debug模式打开，如果已经打开了debug，下面四行代码可以注释掉
    chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
    debugging_port = "--remote-debugging-port=9999"

    command = f"{chrome_path} {debugging_port}"
    subprocess.Popen(command, shell=True)
    # 设置一个接受返回结果的
    # something: dict

    def intercept_xhr(route: playwright.sync_api.Route):
        route.continue_()
        cookies = route.request.all_headers().get('cookie')
        for kv in cookies.split(';'):
            k = kv.split('=')[0].strip()
            v = kv.split('=')[1].strip()
            # 接收值

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9999")
        content = browser.contexts[0]
        page = content.new_page()

        page.route("**/m-base/sale/shopping*", intercept_xhr)
        page.goto(FILEPATH)

        btn = page.locator('#nc_1_n1z')
        btn_position = btn.bounding_box()
        new_x = btn_position['x'] + 300
        new_y = btn_position['y']
        page.mouse.click(btn_position['x'], btn_position['y'])

        page.mouse.down()
        page.mouse.move(new_x, new_y)
        page.mouse.up()
        # 等待一段时间以观察拖动效果
        page.wait_for_timeout(1000)
        browser.close()

    # 将cookie返回回去
    # return ...
