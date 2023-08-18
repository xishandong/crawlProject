import os
import time
import pickle
from time import sleep
from selenium import webdriver

damai_url = "https://www.damai.cn/"
login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
target_url = 'https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.4aaef91aSAi8dR&id=704282803735&clicktitle=2023%E5%BC%A0%E6%9D%B0%E6%9C%AA%C2%B7LIVE%E2%80%94%E3%80%8C%E6%9B%9C%C2%B7%E5%8C%97%E6%96%97%E3%80%8D%E5%B7%A1%E6%BC%94%E5%B9%BF%E5%B7%9E%E7%AB%99'


# 这里不是我不放，是平台不给放
# 要全部的就来
class Concert:
    def __init__(self):
        self.status = 0
        self.login_method = 1
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')

    def set_cookie(self):
        self.driver.get(damai_url)
        print("###请点击登录###")
        while self.driver.title.find('dm-全球演出赛事官方购票平台') != -1:
            sleep(1)
        print('###请扫码登录###')

        while self.driver.title != 'dm-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(target_url)

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        if self.login_method==0:
            self.driver.get(login_url)
            print('###开始登录###')

        elif self.login_method==1:
            if not os.path.exists('cookies.pkl'):
                self.set_cookie()
            else:
                self.driver.get(target_url)
                self.get_cookie()

    def enter_concert(self):
        """打开浏览器"""
        print('###打开浏览器，进入dm网###')

        self.login()
        self.driver.refresh()
        self.status = 2
        print("###登录成功###")
        if self.isElementExist('/html/body/div[2]/div[2]/div/div/div[3]/div[2]'):
            self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[3]/div[2]').click()

    def isElementExist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(element)
            return flag

        except:
            flag = False
            return flag

    def choose_ticket(self):
        if self.status == 2:
            print("=" * 30)
            print("###开始进行日期及票价选择###")
            while self.driver.title.find('确认订单') == -1:
                try:
                    buybutton = self.driver.find_element_by_class_name('buybtn').text
                    if buybutton == "提交缺货登记":

                        self.status = 2
                        self.driver.get(target_url)
                        print('###抢票未开始，刷新等待开始###')
                        continue
                    elif buybutton == "立即预定":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 3
                    elif buybutton == "立即购买":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 4
                    elif buybutton == "选座购买":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 5
                except:
                    print('###未跳转到订单结算界面###')
                title = self.driver.title
                if title == '选座购买':
                    self.choice_seats()
                elif title == '确认订单':
                    while True:
                        print('waiting ......')
                        if self.isElementExist('//*[@id="container"]/div/div[9]/button'):
                            self.check_order()
                            break

    def choice_seats(self):
        while self.driver.title == '选座购买':
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/img'):
                print('请快速的选择您的座位！！！')
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[2]/div'):
                self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/button').click()

    def check_order(self):
        if self.status in [3, 4, 5]:
            print('###开始确认订单###')
            try:
                self.driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div[2]/div[1]/div/label').click()
            except Exception as e:
                print("###购票人信息选中失败，自行查看元素位置###")
                print(e)
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//div[@class = "w1200"]//div[2]//div//div[9]//button[1]').click()

    def finish(self):
        self.driver.quit()


if __name__ == '__main__':
    try:
        con = Concert()
        con.enter_concert()
        con.choose_ticket()

    except Exception as e:
        print(e)
        con.finish()
