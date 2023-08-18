import requests
from lxml import etree
import urllib3  # 禁用安全请求警告,当目标使用htpps时使用
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 解决爬取网页出现中文乱码的情况
def rebuilt_Language(url, headers):
    response = requests.get(url=url, headers=headers, verify=False)
    #  response.encoding = response.apparent_encoding
    return response


if __name__ == "__main__":
    # UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    # 建立一个文件夹存储照片
    i = -1
    if not os.path.exists('./picLibs'):
        os.mkdir('./picLibs')
    # 设置一个通用的url
    url = 'https://pic.netbian.com/4kmeinv/index_%d.html'
    pageNum = 1
    src_list = []  # 存储图片的src
    img_name_list = []  # 存储图片的名字
    for pageNum in range(1, 3):
        new_url = format(url % pageNum)
        page_text = rebuilt_Language(url=new_url, headers=headers).text
        tree = etree.HTML(page_text)
        # 解析src的属性值，解析alt属性值
        li_list = tree.xpath('//div[@class="wrap clearfix"]//li')
        for li in li_list:
            src = '	https://pic.netbian.com' + li.xpath('./a/img/@src')[0]
            src_list.append(src)
            img_name = li.xpath('./a/img/@alt')[0] + '.jpg'
            # 解决中文乱码的方法
            img_name = img_name.encode('iso-8859-1').decode('gbk')
            img_name_list.append(img_name)
    # 请求图片并持续化存储
    for img_url in src_list:
        i = i + 1
        img_data = requests.get(url=img_url, headers=headers).content
        img_path = 'picLibs/' + img_name_list[i]
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
            print(img_name_list[i] + '下载成功！')
