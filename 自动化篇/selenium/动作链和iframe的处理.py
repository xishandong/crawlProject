from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains

# 创建对象
bro = webdriver.Chrome('chromedriver.exe')
# 指定url
bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')

# 想要定位的标签是存在于iframe之中，则必须通过如下操作再进行标签定位
# div = bro.find_element_by_id('draggable') 错误的方法定位
bro.switch_to.frame('iframeResult')  # 切换到我们想要指定的iframe中
div = bro.find_element_by_id('draggable')

# 动作链
action = ActionChains(bro)
# 点击长按指定的标签
action.click_and_hold(div)
for i in range(5):
    # perform表示立即执行动作链操作
    action.move_by_offset(17, 0).perform()
    sleep(0.3)
# 释放动作链
action.release()

# 退出浏览器
sleep(5)
bro.quit()
