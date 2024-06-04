import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # 打开浏览器后，选择最大化


def auto_buy(username, password, purchase_list_time):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "打开登陆界面")

    driver.get("https://passport.jd.com/new/login.aspx")

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "开始填写账号密码")

    # driver.find_element(By.LINK_TEXT, "账户登录").click()

    driver.find_element(By.NAME, "loginname").send_keys(username)

    driver.find_element(By.NAME, "nloginpwd").send_keys(password)

    driver.find_element(By.ID, "loginsubmit").click()

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "手动拼图验证")

    time.sleep(10)  # 此处睡眠时间用来手动拼图验证

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "登陆成功")

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "等待时间到达抢购时间：", purchase_list_time, "......")

    driver.get("https://cart.jd.com/cart_index")  # 打开购物车并选中商品

    while True:

        count = 0

        for buytime in purchase_list_time:

            nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if nowtime == buytime:

                try:

                    count += 1

                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "开始第 %s 次抢购......" % count)

                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "已打开购物车，选择商品")

                    # 如果没有全选，点击全选

                    if not driver.find_element(By.CLASS_NAME, "jdcheckbox").is_selected():
                        driver.find_element(By.CLASS_NAME, "jdcheckbox").click()

                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "点击去结算")

                    driver.find_element(By.LINK_TEXT, "去结算").click()  # 去结算

                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "点击提交订单")

                    time.sleep(5)  # 提交订单前必须等待几秒【感觉跟电脑性能快慢有关，不卡的电脑可以适当降低尝试】

                    if driver.find_element(By.ID, "order-submit"):
                        driver.find_element(By.ID, "order-submit").click()  # 提交订单

                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "订单提交成功,请前往订单中心待付款付款")

                    continue

                except Exception as e:

                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "抢购出现异常，重新抢购: ", e)

                    continue

        time.sleep(0.001)


if __name__ == '__main__':
    purchase_list_time = [

        "2023-02-27 17:03:00",

        "2023-02-27 17:03:01",

        "2023-02-27 17:03:02",

        "2023-02-27 17:03:03",

        "2023-02-27 17:03:04",

        "2023-02-27 17:03:05",

    ]
    auto_buy('mjlei007@163.com', 'mjlei198613', purchase_list_time)
