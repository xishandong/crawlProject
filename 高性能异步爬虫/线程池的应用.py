import requests
from lxml import etree
from multiprocessing.dummy import Pool
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
# 原则： 线程池处理的是阻塞且耗时的操作
url = 'https://www.pearvideo.com/category_1'

page_text = requests.get(url=url, headers=headers).text
tree = etree.HTML(page_text)
video_src_list = tree.xpath('//*[@id="listvideoListUl"]/li')

for li in video_src_list:
    video_src = 'https://www.pearvideo.com/' + li.xpath('./div[1]/a/@href')[0]
    # print(video_src)
    video_name = li.xpath('./div[1]/a/div[2]/text()')[0]
    # print(video_name)

