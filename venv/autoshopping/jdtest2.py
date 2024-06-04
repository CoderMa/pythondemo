import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from requests.packages.urllib3 import disable_warnings
from requests.cookies import cookiejar_from_dict
import time
import schedule


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("start-maximized")
# # 启动浏览器
# driver = webdriver.Chrome(options=chrome_options)

# 登录京东账号
def login(driver, username, password, login_url):
    driver.get(login_url)
    time.sleep(2)
    # driver.find_element(By.LINK_TEXT, "账户登录").click()
    # time.sleep(2)
    driver.find_element(By.ID, "loginname").send_keys(username)
    driver.find_element(By.ID, "nloginpwd").send_keys(password)
    driver.find_element(By.ID, "loginsubmit").click()
    time.sleep(20)  # 等待手动完成滑块验证等操作


def cookie_info(username, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")

    login_url = "https://passport.jd.com/new/login.aspx"
    driver = webdriver.Chrome(options=chrome_options)
    print("请尽快登录or扫码！")
    # driver.get(login_url)
    login(driver, username, password, login_url)
    time.sleep(15)  # 预留了安全验证的时间
    driver.refresh()  # 刷新页面
    c = driver.get_cookies()
    sessions = dict()
    for cookie in c:
        sessions[cookie['name']] = cookie['value']
    # driver.quit()
    return sessions, driver


class JdSnap:
    def __init__(self, username, password, product_url):
        self.session = requests.Session()
        self.cookie, self.driver = cookie_info(username, password)

        self.session.cookies = cookiejar_from_dict(self.cookie)
        # self.username = username
        # self.password = password
        self.product_url = product_url

        # self.trybuy_interval = float(trybuy_interval)
        # self.Seconds_kill_time = Seconds_kill_time
        # self.number = int(number)

    # 打开商品页面
    def open_product_page(self):
        self.session.get(self.product_url)
        # driver.get(self.product_url)
        time.sleep(10)

    # 加入购物车
    def add_to_cart(self):
        self.driver.find_element(By.ID, "InitCartUrl").click()
        # driver.find_element(By.ID, "InitCartUrl").click()
        time.sleep(10)

    # 进入购物车结算页面
    def checkout(self):
        # self.session.get("https://cart.jd.com/cart.action")
        self.session.get("https://cart.jd.com/cart_index")
        # driver.get("https://cart.jd.com/cart.action")
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "去结算").click()
        # driver.find_element(By.LINK_TEXT, "去结算").click()
        time.sleep(2)

    # 提交订单
    def submit_order(self):
        self.driver.find_element(By.LINK_TEXT, "提交订单").click()
        # driver.find_element(By.LINK_TEXT, "提交订单").click()
        print("订单提交成功！")

    # 定时抢购函数
    def timed_buy1(self):
        # login(username, password)
        self.open_product_page()
        self.add_to_cart()
        self.checkout()
        self.submit_order()


# # 登录京东账号
# def login(username, password):
#     driver.get("https://passport.jd.com/new/login.aspx")
#     time.sleep(2)
#     driver.find_element(By.LINK_TEXT, "账户登录").click()
#     time.sleep(2)
#     driver.find_element(By.ID, "loginname").send_keys(username)
#     driver.find_element(By.ID, "nloginpwd").send_keys(password)
#     driver.find_element(By.ID, "loginsubmit").click()
#     time.sleep(10)  # 等待手动完成滑块验证等操作


# # 定时抢购函数
# def timed_buy(username, password, product_url):
#     login(username, password)
#     open_product_page(product_url)
#     add_to_cart()
#     checkout()
#     submit_order()


if __name__ == "__main__":
    # 修改为您的京东账号和密码
    username = 'mjlei007@163.com'
    password = 'mjlei198613'
    # 修改为您要抢购的商品页面链接
    # product_url = "https://item.jd.com/123456789.html"
    # product_url = "https://item.jd.com/100012043978.html"
    product_url = "https://item.jd.com/272982.html"

    # 设置抢购时间，这里设置为每天的10:00
    # buy_time = "10:00"
    buy_time = "17:13:00"
    client = JdSnap(username, password, product_url)
    client.timed_buy1()

    # 添加定时任务
    # schedule.every().day.at(buy_time).do(timed_buy(), username, password, product_url)
    # schedule.every().day.at(buy_time).do(client.timed_buy1())

    # # 无限循环执行定时任务
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # 关闭浏览器
    client.driver.quit()
