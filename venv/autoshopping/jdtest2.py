import base64
import random
import re
import urllib

import cv2
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests.packages.urllib3 import disable_warnings
from requests.cookies import cookiejar_from_dict
import time
import schedule


def make_browser():
    """获取浏览器驱动"""
    # chrome_options = webdriver.ChromeOptions()
    options = webdriver.ChromeOptions()  # 进入浏览器设置
    # options.add_argument('--headless')  # 无头Chrome,有头更不容易被发现
    options.add_argument('lang=zh_CN.UTF-8')  # 设置中文
    options.add_argument('start-maximized')
    # 设置请求头
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"')
    # 防止打印一些无用的日志
    # options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    # chrome_options.add_argument('--user-data-dir=/dev/null')  # Start with a clean profile
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 避免被检测-无效
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("disable-blink-features=AutomationControlled")  # 去掉了webdriver痕迹
    # options.add_argument('--incognito')  # 隐身模式启动
    # options.add_argument('disable-infobars')  # 隐藏提示语：Chrome正在受到自动软件的控制
    # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('--no-sandbox')
    # 解决DevTools listening on ws...
    options.add_argument('–log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #         # window.navigator.webdriver
    #         # 不加载图片, 提升速度
    #         # options.add_argument('blink-settings=imagesEnabled=false')
    #         # # 指定浏览器分辨率
    # options.add_argument('window-size=1920x3000')
    # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--disable-gpu')

    # chrome_path = "D:\\ouy"
    # browser = webdriver.Chrome(chrome_options=options, executable_path=chrome_path + '/chromedriver.exe', service_log_path=os.devnull)

    browser = webdriver.Chrome(options=options)
    # 移除Selenium中的window.navigator.webdriver
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })
    return browser


# 登录京东账号
def login(driver, username, password, login_url):
    driver.get(login_url)
    time.sleep(2)
    # driver.find_element(By.LINK_TEXT, "账户登录").click()
    # time.sleep(2)
    driver.find_element(By.ID, "loginname").send_keys(username)
    time.sleep(1)
    driver.find_element(By.ID, "nloginpwd").send_keys(password)
    time.sleep(1)
    driver.find_element(By.ID, "loginsubmit").click()
    # time.sleep(20)  # 等待手动完成滑块验证等操作
    driver.implicitly_wait(3)

    wait = WebDriverWait(driver, 10)

    slide_validation(driver, wait)
    time.sleep(5)
    i = 0
    try:
        for i in range(5):
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.JDJRV-suspend-slide")))  # 定位元素
            slide_validation(driver, wait)
            time.sleep(3)
        print(f"试了{i + 1}次都没有成功！！")
    except Exception as e:
        print("验证div不可见验证通过..", e)
        pass


def slide_validation(driver, wait):
    bigimg = 'img_jd/img1.jpg'
    smallimg = 'img_jd/img2.jpg'
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.JDJRV-bigimg > img")))  # 定位元素
    get_img(element, bigimg)

    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.JDJRV-smallimg > img")))  # 定位元素
    get_img(element, smallimg)

    width_web = 242
    width_downloaded = 360
    distance = match(bigimg, smallimg, width_web, width_downloaded, 1)
    slider = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.JDJRV-slide-inner.JDJRV-slide-btn")))
    # slide_slowly2(driver, slider, distance)

    total_slider_length = 202
    if int(distance) > int(total_slider_length / 2):
        slide_slowly(driver, slider, distance, total_slider_length)
    else:
        # slide_slowly2(driver, slider, distance)
        # slowly(driver, slider, distance)
        simulate_slide(driver, slider, distance)


def __add_alpha_channel(img):
    """ 为jpg图像添加alpha通道 """

    r_channel, g_channel, b_channel = cv2.split(img)  # 剥离jpg图像通道
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道

    img_new = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))  # 融合通道
    return img_new


def __handel_img(img):
    """灰度处理，再对图像进行高斯处理，最后进行边缘检"""
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)  # 转灰度图
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # 高斯模糊
    imgCanny = cv2.Canny(imgBlur, 60, 60)  # Canny算子边缘检测
    return imgCanny


def add_img1(img1):
    """
    将http图片保存到本地
    img1：全图url
    """
    urllib.request.urlretrieve(img1, 'img_jd/img1.jpg')


def add_img2(img1, img2):
    """
    将http图片保存到本地
    img1：全图url
    img2：缺口url
    """
    urllib.request.urlretrieve(img1, 'img_jd/img1.jpg')
    urllib.request.urlretrieve(img2, 'img_jd/img2.jpg')


def get_img(img_element, img_path):
    img_encoded = img_element.get_attribute("src")  # 获取元素值
    # pattern = 'background-image: url\\(\\"(.*?)\\"\\);'  # 正则表达式 \\：表示转义
    # pattern = r'data:image/png;base64,(.+)'
    pattern = r"^data:image/\w+;base64,(.+)"
    base64_str = re.findall(pattern, img_encoded, re.S)[0]  # re.S表示点号匹配任意字符，包括换行符
    # Decode the base64 string
    image_data = base64.b64decode(base64_str)

    # Write the binary data to a file
    with open(img_path, "wb") as file:
        file.write(image_data)


def match(img1_path, img2_path, num1=1, num2=1, diff_pixel=2):
    """
    模板匹配，通过openCV分析两个图片的相似度，获取两个相似度很高图片的坐标，从而计算两个图片的距离。
    传入 全图位置、缺口位置、浏览器图片宽度、本地图片宽度 获取到移动距离
    element：元素对象
    img_jpg_path：全图
    img_png_path：缺口
    num1：浏览器图片宽度
    num2：本地图片宽度
    diff_pixel：误差值
    """
    # 读取图像
    img1 = cv2.imread(img1_path, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(img2_path, cv2.IMREAD_UNCHANGED)
    # # 判断jpg图像是否已经为4通道
    if img1.shape[2] == 3:
        # img1 = self.__add_alpha_channel(img1_path)
        img1 = __add_alpha_channel(img1)
    img = __handel_img(img1)
    small_img = __handel_img(img2)

    # res_TM_CCOEFF_NORMED = cv2.matchTemplate(img, small_img, 3)
    res_TM_CCOEFF_NORMED = cv2.matchTemplate(img, small_img, cv2.TM_CCOEFF_NORMED)

    value = cv2.minMaxLoc(res_TM_CCOEFF_NORMED)
    value = value[3][0]  # 获取到移动距离
    # value = value * num1 / num2 - element.location['x']
    value = value * num1 / num2 - diff_pixel
    return value


def slide_slowly(driver, element, distance, total_slider_length=202):
    """
    慢慢滑动滑块模拟人的操作，一次次移动一点点
    传入 浏览器对象、元素位置、移动距离 实现移动滑块
    :param driver: 浏览器对象
    :param element: 元素位置
    :param distance: 移动距离
    :return:
    """
    action = ActionChains(driver)
    action.click_and_hold(element).perform()
    # 先滑动到最右侧然后再反向滑动
    action.move_by_offset(total_slider_length, 0).perform()
    # ActionChains(self.driver).click_and_hold(element).perform()
    # 移动小滑块，模拟人的操作，一次次移动一点点
    i = 0
    moved = 0
    distance = total_slider_length - distance
    while moved < distance:
        # x = random.randint(3, 10)  # 每次移动3到10像素
        x = random.randint(2, 5)  # 每次移动2到5像素

        moved += x
        if moved > distance:
            x -= 1
        action.move_by_offset(xoffset=-x, yoffset=0).perform()
        print("第{}次移动后，位置为{}".format(i, element.location['x']))
        i += 1
        time.sleep(x/100)  # 暂停一段时间来模拟人的滑动动作
    time.sleep(0.7)
    # 移动完之后，松开鼠标
    action.release().perform()
    # driver.implicitly_wait(1)


def slide_slowly2(driver, element, distance):
    """
    慢慢滑动滑块模拟人的操作，一次次移动一点点
    传入 浏览器对象、元素位置、移动距离 实现移动滑块
    :param driver: 浏览器对象
    :param element: 元素位置
    :param distance: 移动距离
    :return:
    """
    action = ActionChains(driver)
    action.click_and_hold(element).perform()
    # ActionChains(self.driver).click_and_hold(element).perform()
    # 移动小滑块，模拟人的操作，一次次移动一点点
    i = 0
    moved = 0
    while moved < distance:
        # x = random.randint(3, 10)  # 每次移动3到10像素
        x = random.randint(2, 5)  # 每次移动2到5像素
        moved += x
        if moved > distance:
            x -= 1
        action.move_by_offset(xoffset=x, yoffset=0).perform()
        print("第{}次移动后，位置为{}".format(i, element.location['x']))
        i += 1
        time.sleep(x/100)  # 暂停一段时间来模拟人的滑动动作
    time.sleep(0.7)
    # 移动完之后，松开鼠标
    action.release().perform()


def slowly(driver, element, distance):
    """
    慢慢滑动滑块模拟人的操作，一次次移动一点点
    传入 浏览器对象、元素位置、移动距离 实现移动滑块
    :param driver: 浏览器对象
    :param element: 元素位置
    :param distance: 移动距离
    :return:
    """
    ActionChains(driver).click_and_hold(element).perform()
    # 移动小滑块，模拟人的操作，一次次移动一点点
    i = 0
    moved = 0
    while moved < distance:
        # # 模拟自然的滑动轨迹
        # track = [random.randint(2, 5) for _ in range(20)]  # 随机生成滑动轨迹
        # print("track:", track)

        # x = random.randint(3, 10)  # 每次移动3到10像素
        x = random.randint(2, 5)  # 每次移动2到5像素
        moved += x
        if moved > distance:
            x -= 1
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        print("第{}次移动后，位置为{}".format(i, element.location['x']))
        time.sleep(x/100)
        i += 1
    # 移动完之后，松开鼠标
    ActionChains(driver).release().perform()

# 模拟滑动
def simulate_slide(driver, slider, distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    v = 0

    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))

    # 滑动滑块
    ActionChains(driver).click_and_hold(slider).perform()
    for x in track:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    ActionChains(driver).release().perform()


def cookie_info(username, password):
    login_url = "https://passport.jd.com/new/login.aspx"

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("start-maximized")
    # driver = webdriver.Chrome(options=chrome_options)

    driver = make_browser()
    print("请尽快登录or扫码！")
    # driver.get(login_url)
    login(driver, username, password, login_url)
    time.sleep(5)  # 预留了安全验证的时间
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
    # client.timed_buy1()

    print(f"open_product_page....{product_url}")
    client.open_product_page()

    # 添加定时任务
    # schedule.every().day.at(buy_time).do(timed_buy(), username, password, product_url)
    # schedule.every().day.at(buy_time).do(client.timed_buy1())

    # # 无限循环执行定时任务
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # 关闭浏览器
    client.driver.quit()
