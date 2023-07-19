import requests
import ddddocr
from lxml import etree

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    # 将验证码图片保存到了本地
    code_img_src = 'https://so.gushiwen.cn/' + tree.xpath('//*[@id="imgCode"]/@src')[0]
    code_data = requests.get(url=code_img_src, headers=headers).content
    with open('./code.jpg', 'wb') as fp:
        fp.write(code_data)
    # 解析验证码
    ocr = ddddocr.DdddOcr()
    with open('code.jpg', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes) # 解析到的验证码数据
