import requests
import json
if __name__ == '__main__':
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }

    place = input('enter a place:')
    page = 1  # 从第1页开始
    fileName = place + 'KFC餐厅位置信息' + '.json'
    for i in range(0, 20):  # 设置一个较大参数直到爬完所有页码
        param = {
            'cname': '',
            'pid': '',
            'keyword': place,  # 查询地点
            'pageIndex': page,  # 查询页码
            'pageSize': '10',  # 每页最多显示10个
        }
        response = requests.post(url=url, params=param, headers=headers)
        page_text = response.text
        # print(page_text)
        with open(fileName, 'a', encoding='utf-8') as fp:
            json.dump(page_text, fp=fp, ensure_ascii=False)
            fp.write('\n')  # 注意这里还是在for循环当中，每爬取完一页内容，就敲个回车
        page = page + 1  # 佛如循环的循环变量，注意前文默认为1
    print('over!!!')