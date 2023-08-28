import playwright.sync_api
from PIL import Image


def run(syncPlayWright: playwright.sync_api.Playwright, url: str, savePath: str, cookies: list[dict]):
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
    # 获取 main 标签的高度
    rectangle = page.wait_for_selector('main')
    box = rectangle.bounding_box()
    main_height = box['height'] + box['y']
    main_left = box['x']
    main_offset = box['y']
    main_width = box['width']
    # 初始化截图列表
    screenshots = []
    # 逐步滚动并截取屏幕截图
    scroll_offset = main_offset
    prev = 0
    scroll_height = 500
    while True:
        # 滚动屏幕
        page.evaluate(f'window.scrollTo({prev}, {scroll_offset})')
        # 截个图
        page.wait_for_timeout(100)
        screenshots.append(page.screenshot(
            clip={"x": main_left, "y": 0, "width": main_width, "height": scroll_height}
        ))
        # 记录上一次的终点
        prev = scroll_offset
        # 判断边界
        if prev < main_height <= prev + scroll_height:
            page.evaluate(f'window.scrollTo(0, {prev})')
            page.wait_for_timeout(100)
            screenshots.append(page.screenshot(
                clip={"x": main_left, "y": 0, "width": main_width, "height": main_height - prev}
            ))
            break
        scroll_offset += scroll_height

    # 将截图拼接在一起
    full_screenshot = Image.new('RGB', (round(main_width), round(box['height'])))
    y_offset = 0
    for index, screenshot in enumerate(screenshots):
        with open(savePath, 'wb') as f:
            f.write(screenshot)
        img = Image.open(savePath)
        full_screenshot.paste(img, (0, y_offset))
        y_offset += img.height
    # 保存完整截图
    full_screenshot.save(savePath)
    page.close()


if __name__ == '__main__':
    cookies = []
    cookie_string = '_csrfToken=;fu=;_yep_uuid=;ywguid=;ywkey=;ywopenid='
    cookie_items = cookie_string.split(';')
    for item in cookie_items:
        name, value = item.split('=')
        cookies.append({'name': name, 'value': value, 'domain': '.qidian.com', 'path': '/'})
    with playwright.sync_api.sync_playwright() as p:
        run(p, 'https://www.qidian.com/chapter/1036094942/764016875/', '10086.png', cookies)
