import re
import requests
import os

# 爬取图片
if __name__ == "__main__":
    # 创建一个文件夹，用来保存所有的图片
    if not os.path.exists('./imgLibs'):
        os.mkdir('./imgLibs')
    url = 'https://www.douban.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    # 使用通用爬虫对url对应的一整张页面进行爬取
    page_text = requests.get(url=url, headers=headers).text
    # 使用聚焦爬虫将页面中所有的图片进行解析、提取
    ex = '<div class="pic">.*?<img src=.*? data-origin="(.*?)" alt=.*?</div>'
    img_src_list = re.findall(ex, page_text, re.S)
    # print(img_src_list)
    for src in img_src_list:
        # 将图片信息以二进制存储
        img_data = requests.get(url=src, headers=headers).content
        # 生成图片名称
        img_name = src.split('/')[-1]
        imgPath = './imgLibs/' + img_name
        with open(imgPath, 'wb') as fp:
            fp.write(img_data)
            print(img_name, '下载成功')
