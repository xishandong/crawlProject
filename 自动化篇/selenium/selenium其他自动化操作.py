import time

from selenium import webdriver
from time import sleep

bro = webdriver.Chrome(executable_path='chromedriver.exe')

if __name__ == '__main__':
    bro = webdriver.Chrome()
    bro.get("https://useragentstring.com/pages/useragentstring.php?name=Chrome")

    bro.quit()

#
# # 标签定位
# search_input = bro.find_element_by_id('q')
# # 标签交互
# search_input.send_keys('iphone')
# sleep(2)
# # 执行一组js程序
#
# bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# sleep(2)
#
# # 点击搜索按钮
# search = bro.find_element_by_class_name('btn-search')
# search.click()
#
# # 切换页面
# bro.get('https://www.baidu.com')
# sleep(2)
# # 回退
# bro.back()
# sleep(2)
# # 前进
# bro.forward()
#
# # 关闭浏览器
# sleep(5)
# bro.quit()
