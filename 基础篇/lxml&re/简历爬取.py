import requests
from lxml import etree
import os

if __name__ == '__main__':
    # UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    url0 = 'https://sc.chinaz.com/jianli/free.html'  # 访问第一页的链接，这里因为直接用free_1无法打开网页
    url = 'https://sc.chinaz.com/jianli/free_%d.html'
    pageNum = 1

    download_list = []
    download_name_list = []
    # 新建文件夹可持续化存储
    if not os.path.exists('./CV_moban'):
        os.mkdir('./CV_moban')
    # 分页爬取
    for pageNum in range(1, 3):
        if pageNum == 1:
            new_url = url0
        else:
            new_url = format(url % pageNum)
        # 实例化对象的构建
        page_text = requests.get(url=new_url, headers=headers).text
        tree = etree.HTML(page_text)
        # 爬取需要下载的页面信息
        CV_infor_list = tree.xpath('//div[@class="main_list jl_main"]/div')
        for cv in CV_infor_list:
            CV_src = cv.xpath('./a/@href')[0]
            CV_text = requests.get(url=CV_src, headers=headers).text
            ctree = etree.HTML(CV_text)
            # 爬取简历下载链接
            download_src = ctree.xpath('//div[@class="down_wrap"]/div[2]/ul/li/a/@href')[0]
            download_list.append(download_src)
            # 爬取简历名称
            download_name = ctree.xpath('//div[@class="bgwhite"]/div//h1/text()')[0]
            download_name = download_name.encode('iso-8859-1').decode('utf-8') + '.rar'
            download_name_list.append(download_name)

    # 批量下载简历模板
    i = -1
    for cvv in download_list:
        i = i + 1
        cvv = download_list[i]
        cv_content = requests.get(url=cvv, headers=headers).content
        cv_path = 'CV_moban/' + download_name_list[i]
        with open(cv_path, 'wb') as fp:
            fp.write(cv_content)
            print(download_name_list[i] + '下载完成！')
