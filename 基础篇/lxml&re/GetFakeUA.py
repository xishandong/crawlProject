import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }

url = 'https://useragentstring.com/pages/useragentstring.php?name=Chrome'

resp = requests.get(url=url, headers=headers).text

tree = etree.HTML(resp)

ul_list = tree.xpath('//*[@id="liste"]/ul')

USER_AGENT = []

fp = open('./fake_UA.txt', 'a', encoding='utf-8')

for ul in ul_list:
    UA = ul.xpath('./li/a/text()')
    for i in range(1, len(UA)):
        ua = '"' + UA[i] + '",\n'
        print(ua)
        fp.write(ua)

fp.close()

