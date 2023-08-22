import os

from playwright.sync_api import sync_playwright

# 打开谷歌浏览器 我们需要将该路径下的快捷方式属性后的目标加上 --remote-debugging-port=9999端口号可改变，与下面创建浏览器的一致即可
chrome_path = r"C:\Users\dongxishan\Desktop\chrome.lnk"
os.startfile(chrome_path)


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
