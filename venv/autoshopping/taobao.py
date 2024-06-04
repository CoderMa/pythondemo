import datetime
import time
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By

d = path.dirname(__file__)
abspath = path.abspath(d)
driver = webdriver.Firefox()
driver.maximize_window()


def login():
    # 打开淘宝登录页，并进行扫码登录

    driver.get("https://www.taobao.com")
    time.sleep(3)

    # if driver.find_element_by_link_text("亲，请登录"):
    if driver.find_element(By.LINK_TEXT, "亲，请登录"):
        driver.find_element(By.LINK_TEXT, "亲，请登录").click()

    print("请在20秒内完成扫码")
    time.sleep(20)

    driver.get("https://cart.taobao.com/cart.htm")

    time.sleep(3)

    # 点击购物车里全选按钮
    # if driver.find_element_by_id("J_CheckBox_939775250537"):
        # driver.find_element_by_id("J_CheckBox_939775250537").click()
    # if driver.find_element_by_id("J_CheckBox_939558169627"):
        # driver.find_element_by_id("J_CheckBox_939558169627").click()
    # if driver.find_element_by_id("J_SelectAll1"):
    if not driver.find_element(By.ID, "J_SelectAll1").is_selected():
        driver.find_element(By.ID, "J_SelectAll1").click()

    now_time = datetime.datetime.now()
    print('login success:', now_time.strftime('%Y-%m-%d %H:%M:%S'))


def buy(buy_time):
    while True:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 对比时间，时间到的话就点击结算
        if now_time >= buy_time:
            try:
                # 点击结算按钮
                if driver.find_element(By.ID, "J_Go"):
                    driver.find_element(By.ID, "J_Go").click()
                    driver.find_element(By.LINK_TEXT, '提交订单').click()
            except Exception as e:
                print(e)
                time.sleep(0.1)

        print(now_time)
        time.sleep(0.1)


if __name__ == "__main__":
    # times = input("请输入抢购时间：")
    # 时间格式："2018-09-06 11:20:00.000000"
    login()
    buy("2024-01-08 20:00:00.000000")
