# UA检测（反爬机制）：门户网站的服务器会检测对应请求的载体身份标识，如果检测到请求的载体身份为某一浏览器，说明该请求是一个正常请求。
# 但是如果检测到不是某一浏览器，则表示该请求为非正常请求。服务器端拒绝该次请求。
# UA：User-Agent（请求载体的身份标识）
# UA伪装：让爬虫身份标识伪装成浏览器
import requests
if __name__ == '__main__':
    # UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    url = 'https://www.sogou.com/web?'
    # 处理url携带的参数：封装到字典中
    kw = input('enter a word:')
    param = {
        'query': kw,
    }
    # 对指定的url发起的请求对应的url是携带参数的，并且请求过程中处理了参数
    response = requests.get(url=url, params=param, headers=headers)

    page_text = response.text
    fileName = kw+ '.html'
    with open(fileName, 'w', encoding='utf-8') as fp:
        fp.write(page_text)
    print(fileName, '保存成功！')
