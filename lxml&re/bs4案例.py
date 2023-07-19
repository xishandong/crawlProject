import requests
from bs4 import BeautifulSoup
import urllib3 # 禁用安全请求警告,当目标使用htpps时使用

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 解决爬取网页出现中文乱码的情况
def rebuilt_Language(url, headers):
    response = requests.get(url=url, headers=headers, verify=False)
    response.encoding = response.apparent_encoding
    return response


# 爬取三国演义小说所有的章节标题和章节内容
if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    page_text = rebuilt_Language(url, headers).text
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(page_text, 'lxml')
    li_list = soup.select('.book-mulu > ul >li')
    fp = open('./sanguo.txt', 'w', encoding='utf-8')
    for li in li_list:
        title = li.a.string
        detail_url = 'https://www.shicimingju.com' + li.a['href']
        detail_page_text = rebuilt_Language(detail_url, headers).text
        # 解析详情页相关章节内容
        detail_soup = BeautifulSoup(detail_page_text, 'lxml')
        div_tag = detail_soup.find('div', class_='chapter_content')
        content = div_tag.text
        fp.write(title + ":" + content + "\n")
        print(title, '爬取成功')
