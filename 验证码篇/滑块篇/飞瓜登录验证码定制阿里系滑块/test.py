import random
from urllib.parse import parse_qs

from playwright.sync_api import Playwright, sync_playwright

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


def run(playwright: Playwright) -> dict:
    result: dict = {}

    # 拦截发送验证码api，把参数截获
    def intercept_xhr(route):
        data = parse_qs(route.request.post_data)
        route.abort()
        # 自行将data传出
        print(data)

    browser = playwright.chromium.connect_over_cdp(WS_URL)
    content = browser.contexts[0]

    page = content.new_page()
    page.route(INTERRUPT_ROUTE, intercept_xhr)
    page.goto(FILEPATH)
    # 进行点击，进入滑块状态
    page.get_by_role("link", name="注册 / 登录").click()
    page.get_by_role("link", name="手机登录").click()
    page.get_by_text("验证码登录").click()
    page.get_by_role("textbox", name="请输入绑定手机号码").click()
    page.get_by_role("textbox", name="请输入绑定手机号码").fill("手机号")
    page.get_by_role("link", name="获取验证码").click()
    # 有可能出现两种id
    try:
        btn = page.locator('#nc_2_n1z')
        btn_position = btn.bounding_box(timeout=10000)
    except:
        btn = page.locator('#nc_1_n1z')
        btn_position = btn.bounding_box()
    # 获取滑动位置
    new_x = btn_position['x'] + random.randint(390, 400)
    new_y = btn_position['y']
    page.mouse.click(btn_position['x'], btn_position['y'])
    # 滑动
    page.mouse.down()
    page.mouse.move(new_x, new_y)
    page.mouse.up()
    # 稍等一下
    page.wait_for_timeout(2000)
    # 关闭所有
    page.close()
    content.close()
    browser.close()
    return result


def main():
    # 用于导出
    with sync_playwright() as playwright:
        a = run(playwright)
    return a


if __name__ == '__main__':
    for _ in range(10):
        print(main())
