import requests
import ddddocr
from lxml import etree

# 获取验证码信息以及页面的隐藏信息，在这里是viewstate和viewstategenerator
if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    # 获取验证码图片连接
    code_img_src = 'https://so.gushiwen.cn/' + tree.xpath('//*[@id="imgCode"]/@src')[0]
    # 获取viewstate的值
    viewstate = tree.xpath("//input[@id='__VIEWSTATE']/@value")[0]
    # 获取viewstategenerator的值
    viewstategenerator = tree.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value")[0]

    # 将验证码图片保存到本地
    # code_data = requests.get(url=code_img_src, headers=headers).content 不可以这样使用，因为一旦请求，原本网页的验证码就会发生改变了
    # 这里我们使用requests中的Session()方法，将请求变成一个对象
    session = requests.Session()
    code_data = session.get(url=code_img_src, headers=headers).content
    with open('./code.jpg', 'wb') as fp:
        fp.write(code_data)
    # 解析验证码
    ocr = ddddocr.DdddOcr()
    with open('code.jpg', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)  # 解析到的验证码数据

    # 模拟登录发送post请求
    login_url = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
    data = {
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        'from': 'http://so.gushiwen.cn/user/collect.aspx',
        'email': '@qq.com',
        'pwd': '',
        'code': res,
        'denglu': '登录',
    }
    # 注意此处也应该用session不然验证码也会刷新
    login_page_text = session.post(url=login_url, data=data, headers=headers).text

    with open('gushiwen.html', 'w', encoding='utf-8') as fp:
        fp.write(login_page_text)
