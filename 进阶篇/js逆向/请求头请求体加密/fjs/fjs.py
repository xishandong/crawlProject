import requests
import execjs
pageNum = 1
# 控制请求的页数
while pageNum < 2:
    # 准备js逆向出请求头和表单签名
    ts = int(execjs.compile(open('sign.js', 'r', encoding='utf-8').read()).call('ts'))
    json_data = {
        'pageNo': pageNum,
        'pageSize': 40,
        'total': 5770,
        'AREACODE': '',
        'M_PROJECT_TYPE': '',
        'KIND': 'GCJS',
        'GGTYPE': '1',
        'PROTYPE': '',
        'timeType': '6',
        'BeginTime': '2022-07-18 00:00:00',
        'EndTime': '2023-01-18 23:59:59',
        'createTime': [],
        'ts': ts,
    }
    sign = str(execjs.compile(open('sign.js', 'r', encoding='utf-8').read()).call('sign', json_data))
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://ggzyfw.fujian.gov.cn',
        'Referer': 'https://ggzyfw.fujian.gov.cn/business/list/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'portal-sign': sign,
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # 发起请求
    response = requests.post('https://ggzyfw.fujian.gov.cn/FwPortalApi/Trade/TradeInfo', headers=headers, json=json_data).json()
    data = response['Data']

    # 解密文件
    ctx = execjs.compile(open('demo.js', 'r', encoding='utf-8').read()).call('decrypt', data)
    print(ctx)
    pageNum += 1
