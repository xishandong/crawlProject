from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains

bro = webdriver.Chrome(executable_path='chromedriver.exe')

bro.get('https://qzone.qq.com')

# 切换作用域
bro.switch_to.frame('login_frame')
# 标签定位与点击
pwdLogin = bro.find_element_by_id('switcher_plogin')
pwdLogin.click()

# 输入账号密码
zhanghao = bro.find_element_by_id('u')
zhanghao.send_keys('')
pwd = bro.find_element_by_id('p')
pwd.send_keys('')

login = bro.find_element_by_id('login_button')
login.click()

sleep(5)
bro.quit()
