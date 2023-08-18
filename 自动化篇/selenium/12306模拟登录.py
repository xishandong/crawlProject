from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions

# 实现让selenium规避被检测到的风险
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])
option.add_experimental_option("excludeSwitches", ['enable-automation'])
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-shm-usage")
option.add_argument("--window-size=1920,1080")  # 建议设置窗口大小
# option.add_argument('--headless')
option.add_argument('--disable-gpu')

bro = webdriver.Chrome(executable_path='chromedriver.exe', options=option)




# 去除特征识别 防止服务器识别到的selenium的特征从而阻止后续的滑动验证
bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

bro.get('https://kyfw.12306.cn/otn/resources/login.html')
bro.maximize_window()

# 标签定位
user = bro.find_element_by_id('J-userName')
pwd = bro.find_element_by_id('J-password')

# 传入数据
user.send_keys('')
sleep(1)
pwd.send_keys('')
sleep(1)

# 登录
login = bro.find_element_by_id('J-login')
login.click()
sleep(2)

slide = bro.find_element('id', 'nc_1_n1z')

# 验证码
action = ActionChains(bro)
action.click_and_hold(slide)
action.move_by_offset(300, 0).perform()
sleep(2)
# 点击确定
ok = bro.find_element_by_class_name('btn')
ok.click()
sleep(2)

ticket = bro.find_element_by_id('link_for_ticket')
ticket.click()
sleep(2)

# 输入查询车站
From = bro.find_element_by_id('fromStationText')
From.click()
From.send_keys('泸州')
From.send_keys(Keys.ENTER)
sleep(0.5)

To = bro.find_element_by_id('toStationText')
To.click()
To.send_keys('乐山')
To.send_keys(Keys.ENTER)
sleep(0.5)

# 找到出发站、到达站的隐藏HTML标签
js = "document.getElementById('train_date').removeAttribute('readonly')"  # 去除日期栏只读属性
bro.execute_script(js)

# 选择日期
data = bro.find_element_by_id('train_date')
data.clear()
data.send_keys('2022-12-31')
data.send_keys(Keys.ENTER)
sleep(0.5)

# 查询
find = bro.find_element_by_id('query_ticket')
find.click()
sleep(2)

# 关闭浏览器
# sleep(5)
# bro.quit()
