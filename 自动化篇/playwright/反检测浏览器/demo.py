from playwright.sync_api import sync_playwright

# stealth.min.js文件的存放路径
STEALTH_PATH = 'stealth.min.js'

with sync_playwright() as p:
    # 创建一个正常的浏览器窗口
    browser = p.chromium.launch(
        headless=False,
        chromium_sandbox=False,
        ignore_default_args=["--enable-automation"],
        channel="chrome",
    )
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    content = browser.new_context(user_agent=ua)
    # 添加初始化脚本
    content.add_init_script(path=STEALTH_PATH)
    # 创建页面
    page = content.new_page()
    page.goto('https://bot.sannysoft.com/')
    # 查看效果，和浏览器一致
    page.wait_for_timeout(5000)
    # 关闭所有
    page.close()
    content.close()
    browser.close()
