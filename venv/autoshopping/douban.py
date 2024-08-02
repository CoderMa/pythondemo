import random
import re
import time
import urllib
import numpy as np
# import schedule
# from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import base64
import cv2


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


class CrackSlider(object):
    """
    滑动验证码工具
    1、add_alpha_channel：为jpg图像添加alpha通道
    2、handel_img：灰度处理，再对图像进行高斯处理，最后进行边缘检
    3、match：获取到移动距离
    """

    def __init__(self):
        self.driver = make_browser()
        self.driver.maximize_window()

    def __add_alpha_channel(self, img):
        """ 为jpg图像添加alpha通道 """

        r_channel, g_channel, b_channel = cv2.split(img)  # 剥离jpg图像通道
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道

        img_new = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))  # 融合通道
        return img_new

    def __handel_img(self, img):
        """灰度处理，再对图像进行高斯处理，最后进行边缘检"""
        imgGray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)  # 转灰度图
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # 高斯模糊
        imgCanny = cv2.Canny(imgBlur, 60, 60)  # Canny算子边缘检测
        return imgCanny

    def match(self, element, img1_path, img2_path, num1, num2):
        """
        模板匹配，通过openCV分析两个图片的相似度，获取两个相似度很高图片的坐标，从而计算两个图片的距离。
        传入 全图位置、缺口位置、浏览器图片宽度、本地图片宽度 获取到移动距离
        element：元素对象
        img_jpg_path：全图
        img_png_path：缺口
        num1：浏览器图片宽度
        num2：本地图片宽度
        """
        # 读取图像
        img1 = cv2.imread(img1_path, cv2.IMREAD_UNCHANGED)
        img2 = cv2.imread(img2_path, cv2.IMREAD_UNCHANGED)
        # 判断jpg图像是否已经为4通道
        if img1.shape[2] == 3:
            # img1 = self.__add_alpha_channel(img1_path)
            img1 = self.__add_alpha_channel(img1)
        img = self.__handel_img(img1)
        small_img = self.__handel_img(img2)
        res_TM_CCOEFF_NORMED = cv2.matchTemplate(img, small_img, 3)
        value = cv2.minMaxLoc(res_TM_CCOEFF_NORMED)
        value = value[3][0]  # 获取到移动距离
        value = value * num1 / num2 - element.location['x']
        return value

    def get_pos(self, element, img1, num, num1, num2, diff_pixel=4):
        """
        轮廓检测，通过openCV进行轮廓检测，即在大图片中找到缺口位置的坐标，然后计算小图片到缺口位置的距离。
        传入 图片、缺口像素、浏览器图片宽度、本地图片宽度 获取移动像素
        :param element: 元素位置
        :param img1: 图片地址
        :param num: 图片缺口长宽像素，基本上长宽必须一致
        :param num1: 浏览器图片宽度
        :param num2: 本地图片宽度
        :param diff_pixel: 滑块按钮和缺块 x坐标的差值
        :return: 缺口x坐标
        """
        # 读取图像文件并返回一个image数组表示的图像对象
        image = cv2.imread(img1)
        # GaussianBlur方法进行图像模糊化/降噪操作。
        # 它基于高斯函数（也称为正态分布）创建一个卷积核（或称为滤波器），该卷积核应用于图像上的每个像素点。
        blurred = cv2.GaussianBlur(image, (5, 5), 0, 0)
        # Canny方法进行图像边缘检测
        # image: 输入的单通道灰度图像。
        # threshold1: 第一个阈值，用于边缘链接。一般设置为较小的值。
        # threshold2: 第二个阈值，用于边缘链接和强边缘的筛选。一般设置为较大的值
        canny = cv2.Canny(blurred, 0, 100)  # 轮廓
        # findContours方法用于检测图像中的轮廓,并返回一个包含所有检测到轮廓的列表。
        # contours(可选): 输出的轮廓列表。每个轮廓都表示为一个点集。
        # hierarchy(可选): 输出的轮廓层次结构信息。它描述了轮廓之间的关系，例如父子关系等。
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 遍历检测到的所有轮廓的列表
        for contour in contours:
            # contourArea方法用于计算轮廓的面积
            area = cv2.contourArea(contour)
            # arcLength方法用于计算轮廓的周长或弧长
            length = cv2.arcLength(contour, True)
            # 如果检测区域面积在原来基础上下百分之四之间，周长在原来基础上下百分之四之间，则是目标区域
            if num * num - num * num / 4 < area < num * num + num * num / 4 and num * 4 - num * 4 / 4 < length < num * 4 + num * 4 / 4:
                # 计算轮廓的边界矩形，得到坐标和宽高
                # x, y: 边界矩形左上角点的坐标。
                # w, h: 边界矩形的宽度和高度。
                x, y, w, h = cv2.boundingRect(contour)
                print("计算出目标区域的坐标及宽高：", x, y, w, h)
                # 在目标区域上画一个红框看看效果
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.imwrite("img/test.jpg", image)
                return x * num1 / num2 - element.location['x'] - diff_pixel
        return 0

    def add_img1(self, img1):
        """
        将http图片保存到本地
        img1：全图url
        """
        urllib.request.urlretrieve(img1, 'img/img1.jpg')

    def add_img2(self, img1, img2):
        """
        将http图片保存到本地
        img1：全图url
        img2：缺口url
        """
        urllib.request.urlretrieve(img1, 'img/img1.jpg')
        urllib.request.urlretrieve(img2, 'img/img2.jpg')

    def slowly(self, driver, element, distance):
        """
        慢慢滑动滑块模拟人的操作，一次次移动一点点
        传入 浏览器对象、元素位置、移动距离 实现移动滑块
        :param driver: 浏览器对象
        :param element: 元素位置
        :param Dis: 移动距离
        :return:
        """
        ActionChains(driver).click_and_hold(element).perform()
        # 移动小滑块，模拟人的操作，一次次移动一点点
        i = 0
        moved = 0
        while moved < distance:
            x = random.randint(3, 10)  # 每次移动3到10像素
            moved += x
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
            print("第{}次移动后，位置为{}".format(i, element.location['x']))
            time.sleep(0.2)
            i += 1
        # 移动完之后，松开鼠标
        ActionChains(driver).release().perform()

    def login(self):
        self.driver.get("https://accounts.douban.com/passport/login")  # 打开豆瓣登录页面
        self.driver.implicitly_wait(5)  # 隐式等待5秒
        element = self.driver.find_element(By.XPATH, "//li[text()='密码登录']")  # 定位【密码登录】元素
        element.click()  # 点击确认

        time.sleep(3)

        username = "18019101737"
        password = "mjlei!@0051"
        element = self.driver.find_element(By.XPATH, "//input[@id='username']")  # 定位元素
        element.send_keys(username)  # 输入内容
        time.sleep(1)
        element = self.driver.find_element(By.XPATH, "//input[@id='password']")  # 定位元素
        element.send_keys(password)  # 输入内容
        time.sleep(1)
        element = self.driver.find_element(By.XPATH, "//a[text()='登录豆瓣']")  # 定位元素
        element.click()  # 点击按钮

        self.driver.implicitly_wait(5)  # 隐式等待5秒
        self.driver.switch_to.frame("tcaptcha_iframe_dy")  # 切换到frame区域
        time.sleep(3)

        # element = self.driver.find_element(By.XPATH, "//div[@id='slideBg']")  # 定位元素
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='slideBg']")))  # 定位元素
        style = element.get_attribute("style")  # 获取元素值
        pattern = 'background-image: url\\(\\"(.*?)\\"\\);'  # 正则表达式 \\：表示转义
        img1 = re.findall(pattern, style, re.S)[0]  # re.S表示点号匹配任意字符，包括换行符
        print("滑块验证图片下载路径:", img1)  # 打印结果
        self.add_img1(img1)  # 下载图片

        # # 实例化一个类对象
        # cs = CrackSlider()

        # 准备方法需要的入参
        # 1、找到滑动按钮位置
        element_slider = self.driver.find_element(By.XPATH, "//div[@class='tc-fg-item tc-slider-normal']")
        # 2、图片位置（相对当前项目）
        img = 'img/img1.jpg'
        # 3、缺口像素长宽（长宽必须一致）
        gap_wide = 80
        # 4、web图片宽度
        web_wide = 340
        # 5、原图片宽度
        raw_wide = 672
        # 调用方法获取返回的移动距离
        dis = self.get_pos(element_slider, img, gap_wide, web_wide, raw_wide)
        # 打印一下移动距离
        print("dis=", dis)

        # 调用方法移动滑块致缺口位置
        # driver 浏览器驱动对象
        # element 元素位置对象
        # dis 移动距离
        cs.slowly(self.driver, element_slider, dis)
        # 整体等待5秒看结果
        # time.sleep(5)
        time.sleep(15)
        # 关闭浏览器
        self.driver.quit()

    def test(self):
        distance = self.match(None, "huakuai/bg.jpg", "huakuai/quekuai_realsize.jpg", 1, 1)


if __name__ == '__main__':
    # 实例化一个类对象
    cs = CrackSlider()
    cs.login()
