import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    # 将本地的html文件中的数据加载到该对象中
    fp = open('test.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(fp, 'lxml')
    # print(soup)
    # print(soup.a) # soup.tagName 返回的是html中第一次出现的tagName标签
    # print(soup.find('div')) # 相当于soup.div
    # print(soup.find('div', class_='song'))
    # print(soup.find_all('a'))
    # print(soup.select('.tang'))
    # print(soup.select('.tang > ul > li > a')[0])
    # print(soup.select('.tang > ul a')[0])
    # print(soup.select('.tang > ul a')[0].text)
    tag = soup.find('div', class_='song')
    print(tag.text)