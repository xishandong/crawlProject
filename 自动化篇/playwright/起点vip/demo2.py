import playwright.sync_api


def run(syncPlayWright: playwright.sync_api.Playwright, url: str, savePath: str, cookies: list[dict]):
    run_js = 'document.getElementById("navbar").remove();'
    browser = syncPlayWright.chromium.launch(
        headless=False,
        chromium_sandbox=False,
        channel="chrome",
    )
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    content = browser.new_context(user_agent=ua)
    content.add_init_script(path=r'D://crawlProjects/stealth.min.js')
    content.add_cookies(cookies)
    page = content.new_page()
    page.goto(url)
    page.evaluate(run_js)
    page.locator(".print").screenshot(path="screenshot.png", animations='disabled')
    page.close()


if __name__ == '__main__':
    cookies = []
    cookie_string = ''
    cookie_items = cookie_string.split(';')
    for item in cookie_items:
        name, value = item.split('=')
        cookies.append({'name': name, 'value': value, 'domain': '.qidian.com', 'path': '/'})
    with playwright.sync_api.sync_playwright() as p:
        run(p, 'https://www.qidian.com/chapter/1035571469/733045990/', '10086.png', cookies)
