from playwright.sync_api import sync_playwright

import subprocess

# 这个路径可以是Google浏览器的exe路径，也可以是快捷方式的路径
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
debugging_port = "--remote-debugging-port=9999"

command = f"{chrome_path} {debugging_port}"
subprocess.Popen(command, shell=True)


# 拦截请求
def intercept_xhr(route, request):
    route.continue_()
    response = route.fetch()
    json = response.json()
    print(json)


with sync_playwright() as p:
    # 创建一个连接
    browser = p.chromium.connect_over_cdp("http://localhost:9999")
    content = browser.contexts[0]
    page = content.new_page()

    # 设置拦截规则
    page.route("**/api/sns/web/v1/homefeed", lambda route, request: intercept_xhr(route, request))
    page.goto('https://www.xiaohongshu.com/')
    page.wait_for_selector('.feeds-container')

    # 获取页面内容高度
    page_height = page.evaluate('() => document.body.scrollHeight')

    # 模拟鼠标滚动操作，向下滚动到底部
    while page.evaluate('() => window.scrollY + window.innerHeight') < page_height:
        page.mouse.wheel(0, 100)  # 这里的参数可以根据需要进行调整

    page.wait_for_timeout(5000)
