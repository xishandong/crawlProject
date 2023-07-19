import requests
from lxml import etree

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    # 设置一个通用的url
    url = 'https://sh.58.com/ershoufang/p%d/?PGTID=0d30000c-0000-2e04-d18a-9af183e2d6a4&ClickID=1'
    pageNum = 1
    fp = open('58.txt', 'w', encoding='utf-8')
    for pageNum in range(1, 9):
        new_url = format(url % pageNum) # 拼接成完整的url
        page_text = requests.get(url=new_url, headers=headers).text
        tree = etree.HTML(page_text)
        tongji_list = tree.xpath('//section[@class="list"]/div')
        for li in tongji_list:
            title = li.xpath('./a/div[2]//h3/text()')[0]
            print(title)
            fp.write(title + '\n')
    print('over!')