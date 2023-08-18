from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep

# 实现让selenium规避被检测到的风险
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
# 实现无可视化界面的操作
option.add_argument('--headless')
option.add_argument('--disable-gpu')

bro = webdriver.Chrome(executable_path='chromedriver.exe', options=option)

# 无可视化界面（无头浏览器） phantomJs
bro.get('https://www.baidu.com')
print(bro.page_source)

# 关闭浏览器
sleep(5)
bro.quit()

