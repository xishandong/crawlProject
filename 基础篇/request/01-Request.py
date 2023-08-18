# requests模块的使用
import requests

if __name__ == "__main__":
    # 指定url
    url = 'https://wz.sun0769.com/political/index/politicsNewest'
    # 发起请求
    # get方法会返回一个响应对象
    response = requests.get(url=url)
    # 获取响应数据
    page_txt = response.text
    # 持久化存储
    with open('./sogou.html', 'w', encoding='utf-8') as fp:
        fp.write(page_txt)
    print('爬取数据结束！')

