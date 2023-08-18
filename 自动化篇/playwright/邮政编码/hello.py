import pandas as pd
from playwright.sync_api import sync_playwright, Error


def getCode(addr):
    # 用同步的方式打开一个浏览器
    with sync_playwright() as p:
        try:
            # 设置浏览器配置
            browser = p.chromium.launch(headless=True)
            # 打开一个新窗口
            page = browser.new_page()
            # 去往这个链接
            page.goto('https://www.youbianku.com/%E9%A6%96%E9%A1%B5')
            # 等待页面加载完毕
            page.wait_for_load_state('load')
            # 通过id选中input框
            search_input = page.query_selector("#mySearchInput")
            # 往input框输入数据
            search_input.type(addr)
            # 通过id选择按钮
            search_button = page.query_selector("#mySearchButton")
            # 按钮点击
            search_button.click()
            # 表格选择器
            table_selector = ".zipcode-datas"
            # 等待表格渲染完毕
            page.wait_for_selector(table_selector, timeout=5000)
            # 通过class选择表格
            table = page.query_selector(table_selector)
            # 根据表格的类选择不同的行
            if "top-space" in table.get_attribute("class"):
                postal_code_selector = "tr:nth-child(5) td a"
            else:
                postal_code_selector = "tr:nth-child(3) td a"
            # 获取邮政编码所在的行
            postal_code_element = table.query_selector(postal_code_selector)
            # 获取邮政编码
            return postal_code_element.inner_text()
        except Error as e:
            # 捕获异常，出现地址错误可能表格无法加载
            print(e)
            return '000000'
        finally:
            # 关闭浏览器
            browser.close()


if __name__ == '__main__':
    # 定义一个地址存储器，每次先从里面查找，找不到再去请求
    storgeCode = {
    }
    # 打开文佳佳
    fileA = pd.read_excel('./file.xlsx')
    # 修改格式
    new_header = fileA.iloc[0]
    fileA.columns = new_header
    # 遍历文件
    for index, row in fileA.iterrows():
        address = row['通讯地址']
        # 判断地址是否为空
        if pd.notna(address) and address != '通讯地址':
            if storgeCode.get(address, None) is None:
                # 找不到，就去请求
                code = getCode(address)
                storgeCode[address] = code
            postal_code = storgeCode[address]
            fileA.at[index, '邮政编码'] = postal_code
        else:
            continue
        # 每次修改后打印一下
        print(fileA.iloc[index]['姓名'], fileA.iloc[index]['通讯地址'], fileA.iloc[index]['邮政编码'])
    # 保存修改
    fileA.to_excel('updated_file.xlsx', index=False)
