import asyncio
import re
import time
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict, Union
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Error


class StoreInfo(TypedDict):
    url: str
    email: Union[str, None]
    phone: Union[str, None]
    googleMapLink: Union[str, None]
    googleMapInfo: Union[str, None]
    instagramLink: Union[str, None]
    twitterLink: Union[str, None]
    youtubeLink: Union[str, None]
    pinterestLink: Union[str, None]
    snapchatLink: Union[str, None]
    linkedinLink: Union[str, None]
    facebookLink: Union[str, None]


excluded_resource_types = ['image', 'Media', 'font']


async def block_aggressively(route):
    if route.request.resource_type in excluded_resource_types:
        await route.abort()
    else:
        await route.continue_()


async def do_browser(_url, page):
    try:
        await page.goto(_url, timeout=20000)
        await page.wait_for_load_state('load', timeout=5000)
        iframes = await page.query_selector_all('iframe')
        for _ in iframes:
            await asyncio.sleep(2.5)
        return await page.content()
    except Error as e:
        error_message = str(e)
        if "net::ERR_CONNECTION_CLOSED" in error_message:
            print('网络链接错误: ', _url)
            return do_browser(_url, page)
        elif "net::ERR_CERT_COMMON_NAME_INVALID" in error_message:
            return ''
        elif 'net::ERR_ABORTED' in error_message:
            return ''
        elif 'Timeout' in error_message:
            try:
                return await page.content()
            except Exception as e:
                print(e)
                return ''
        print('--------------------------------')
        print(e)
        print('出现错误: ', _url)
        print('--------------------------------')
        return ''


async def get_html_content(_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({"Cache-Control": "max-age=3600"})
        await page.route("**/*", block_aggressively)
        page_source = await do_browser(_url, page)
        sub_links = parse_sub_link(_url, page_source)
        for link in sub_links[:10]:
            page_source += await do_browser(link, page)
        await browser.close()
        return page_source


def parse_email(html_content):
    # 匹配邮箱
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email_matches = re.findall(email_pattern, html_content, re.I)
    return ' | '.join(list(set(email_matches)))


def parse_phone(html_content):
    # 定义不同国家/地区的手机号正则表达式模板
    phone_patterns = [
        re.compile(r'\+1\s(\d{3})[ -](\d{3})[ -](\d{4})'),
        re.compile(r'\((\d{3})\)[ -](\d{3})[ -](\d{4})'),
        re.compile(r'\+44\s\d{2}\s\d{4}\s\d{4}'),
        re.compile(r'\+86\s\d{2}\s\d{8}'),
        re.compile(r'\+33\s\d\s\d{2}\s\d{2}\s\d{2}\s\d{2}'),
        re.compile(r'(\d{3})[ -](\d{3})[ -](\d{4})'),
        re.compile(r'\((\d{3})\)\s?(\d{3})[ -](\d{4})'),
        re.compile(r'\++\s?\(?8?6?\s?1[3-9]\d{9}'),
    ]
    # 在文档中匹配手机号
    phone_matches = []
    final_matches = []
    for pattern in phone_patterns:
        matches = pattern.findall(html_content)
        phone_matches.extend(matches)
    for phone in phone_matches:
        if isinstance(phone, tuple):
            final_matches.append('-'.join(phone))
        else:
            final_matches.append(phone)
    return ' | '.join(list(set(final_matches)))


def parse_link(html_content):
    # 定义要匹配的平台域名
    platform_domains = {
        "facebook.com", "instagram.com", "twitter.com", "youtube.com",
        "pinterest.com", "snapchat.com", "linkedin.com",
        "www.facebook.com", "www.instagram.com", "www.twitter.com",
        "www.youtube.com", "www.pinterest.com", "www.snapchat.com",
        "www.linkedin.com",
    }
    # 创建字典来存储不同网站的链接列表
    categorized_links = {
        "facebook": [],
        "instagram": [],
        "twitter": [],
        "youtube": [],
        "pinterest": [],
        "snapchat": [],
        "linkedin": [],
    }
    # 用于存储匹配的链接
    matched_links = []
    # 提取链接并匹配域名
    pattern = r'href=["\'](https?://(?:www\.)?\w+\.\w+[^"\']*)["\']'
    matches = re.findall(pattern, html_content, re.I)
    for link in matches:
        parsed = urlparse(link)
        if parsed.netloc in platform_domains:
            matched_links.append(link)
    final_links = list(set(matched_links))
    for link in final_links:
        parsed = urlparse(link)
        domain = parsed.netloc.replace('www.', '').replace('.com', '')
        categorized_links[domain].append(link)
    return categorized_links


def parse_google_map(html_content):
    area_pattern = r'coords="([^"]*)"[^>]*title="([^"]*)"'
    iframe_pattern = r'<iframe[^>]*src=["\'](https?://(?:www\.)?(?:google\.com/maps|maps\.google\.com)[^"]*)["\'][^>]*>'
    google_map_link = r'href="(https?://(?:www\.)?(?:google\.com/maps|maps\.google\.com)[^"]*)"'
    matches = re.findall(google_map_link, html_content)
    iframe_matches = re.findall(iframe_pattern, html_content, re.I)
    area_matches = re.findall(area_pattern, html_content, re.I)
    if matches:
        iframe_matches.extend(list(set(matches)))
    if iframe_matches:
        iframe_matches = list(set(iframe_matches))
    area_info = []
    if area_matches:
        area_matches = list(set(area_matches))
        for match in area_matches:
            coord, title = match
            area_info.append(f'{title}: {coord}')
    return ' | '.join(iframe_matches), ' | '.join(area_info)


def parse_sub_link(_url: str, html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    # 获取所有 <a> 标签的 href 属性
    sub_links = []
    main_domain = urlparse(_url).netloc.replace('www.', '').replace('.com', '')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            try:
                domain = urlparse(href).netloc.replace('www.', '').replace('.com', '')
                if not domain and href != '/' and href.startswith('/'):
                    sub_links.append(_url + href)
                elif domain == main_domain and href.replace('www.', '') != _url.replace('www.', ''):
                    sub_links.append(href)
            except TypeError:
                print('error: ', href)
    return list(set(sub_links))


async def sigal_page_async(_url):
    saveData: StoreInfo
    content = await get_html_content(_url)
    emails = parse_email(content)
    phones = parse_phone(content)
    links = parse_link(content)
    mapLink, mapInfo = parse_google_map(content)
    saveData = {
        'url': _url,
        'phone': phones,
        'email': emails,
        'googleMapLink': mapLink,
        'googleMapInfo': mapInfo,
        'instagramLink': ' | '.join(links['instagram']),
        'twitterLink': ''.join(links['twitter']),
        'youtubeLink': ''.join(links['youtube']),
        'snapchatLink': ''.join(links['snapchat']),
        'facebookLink': ''.join(links['facebook']),
        'linkedinLink': ''.join(links['linkedin']),
        'pinterestLink': ''.join(links['pinterest']),
    }
    print('===================================')
    print(saveData)
    print('====================================')


def sigal_page(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(sigal_page_async(url))
    loop.close()


def main():
    urls = [
        'https://marthascraftyideas.com',
        'https://007-barbershop.com',
        'https://028barbershop.com',
        'https://1stclassbarbershop.com',
        'https://3kingsbarbers.com',
        'https://402barbershop.setmore.com',
        'https://adoreme.com',
        'https://afrobarbershop.com',
        'https://alexsclassicbarbershop.com'
    ]

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(sigal_page, url) for url in urls]
        for future in futures:
            future.result()


if __name__ == '__main__':
    a = time.time()
    main()
    b = time.time()
    print(b - a)
