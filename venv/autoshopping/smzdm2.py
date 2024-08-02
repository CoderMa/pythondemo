import random
import time

import numpy as np
import schedule
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
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
    # options.add_argument('--disable-gpu')

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


class SMZDM:
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

    def match(self, img1_path, img2_path, num1=1, num2=1):
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
        # # 判断jpg图像是否已经为4通道
        if img1.shape[2] == 3:
            # img1 = self.__add_alpha_channel(img1_path)
            img1 = self.__add_alpha_channel(img1)
        img = self.__handel_img(img1)
        small_img = self.__handel_img(img2)
        # small_img = img2

        # res_TM_CCOEFF_NORMED = cv2.matchTemplate(img, small_img, 3)
        res_TM_CCOEFF_NORMED = cv2.matchTemplate(img, small_img,  cv2.TM_CCOEFF_NORMED)

        value = cv2.minMaxLoc(res_TM_CCOEFF_NORMED)
        value = value[3][0]  # 获取到移动距离
        # value = value * num1 / num2 - element.location['x']
        value = value * num1 / num2
        return value

    def identify_gap(self, bg, tp, out):
        """
        bg: 背景图片
        tp: 缺口图片
        out:输出图片
        """
        # 读取背景图片和缺口图片
        bg_img = cv2.imread(bg)  # 背景图片
        tp_img = cv2.imread(tp)  # 缺口图片
        # 识别图片边缘
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)
        # 转换图片格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
        # 缺口匹配
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
        # 绘制方框
        th, tw = tp_pic.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite(out, bg_img)  # 保存在本地
        print("identify_gap 方法返回的缺口的X坐标:", tl[0])
        # 返回缺口的X坐标
        return tl[0]

    def get_element_slide_distance(self, slider_path, bg_path):
        slider_pic = cv2.imread(slider_path, 0)
        bg_pic = cv2.imread(bg_path, 0)
        width, height = slider_pic.shape[::-1]
        slider01 = "./huakuai/slider01.jpg"
        bg01 = "./huakuai/bg01.jpg"

        cv2.imwrite(slider01, slider_pic)
        cv2.imwrite(bg01, bg_pic)

        # 读取另存的滑块图
        slider_pic = cv2.imread(slider01)
        # 进行色彩转换, 转灰度图
        slider_pic = cv2.cvtColor(slider_pic, cv2.COLOR_BGR2GRAY)
        # 高斯模糊
        slider_pic = cv2.GaussianBlur(slider_pic, (5, 5), 1)
        # Canny算子边缘检测
        slider_pic = cv2.Canny(slider_pic, 60, 60)
        # slider_pic = abs(255 - slider_pic)
        cv2.imwrite(slider01, slider_pic)
        slider_pic = cv2.imread(slider01)
        bg_pic = cv2.imread(bg01)

        # 比较两张图的重叠区域
        result = cv2.matchTemplate(slider_pic, bg_pic, cv2.TM_CCOEFF_NORMED)
        top, left = np.unravel_index(result.argmax(), result.shape)
        print("当前滑块的缺口位置：", (left, top, left + width, top + height))
        return left

    def crop_image(self, image_path='huakuai/quekuai.jpg'):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # 将图像转换为二值图
        _, thresh = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
        # 查找轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # 找到最大的轮廓，即非空白区域
        cnt = max(contours, key=cv2.contourArea)
        # 获取最小外接矩形边界
        x, y, w, h = cv2.boundingRect(cnt)
        # 裁剪图像
        cropped_image = image[y:y + h, x:x + w]
        # 进行色彩转换, 转灰度图
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_GRAY2RGB)
        return cropped_image

    def test_login(self):
        login_url = "https://www.smzdm.com/"
        # self.session = requests.Session()
        # self.cookie = cookie_info(self.login_url)
        # self.session.cookies = cookiejar_from_dict(self.cookie)
        self.driver.get(login_url)
        time.sleep(1)

        # self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[3]/div[1]/div[2]/div[1]/a').click()
        print(".....")
        self.driver.find_element(By.XPATH, "//a[text() = '登录'][1]").click()

        time.sleep(3)
        self.driver.switch_to.frame('J_login_iframe')
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]").click()
        time.sleep(1)

        account = "mjlei007@163.com"
        password = "mjlei!@0051"

        # account = "18019101737"
        # password = "mjlei1qaz2wsx"

        self.driver.find_element(By.ID, "username").send_keys(account)
        time.sleep(1)
        self.driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(1)
        self.driver.find_element(By.ID, "loginAgreement").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "login_submit").click()

        # self.driver.switch_to.frame('J_login_iframe')
        # windows = self.driver.window_handles  # 所有窗口句柄
        # # 切换到验证窗口
        # self.driver.switch_to.window(windows[-1])

        wait = WebDriverWait(self.driver, 10)
        div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.geetest_panelshowslide")))
        # 找到滑块元素
        slider = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.geetest_slider_button')))
        # slider = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.geetest_slider_button')))

        # self.driver.save_screenshot("./huakuai/screenshot.png")
        # # 获取滑块初始位置和结束位置
        # left = slider.location['x']
        # width = slider.size['width']
        #
        # # 执行滑动操作 Scroll the slider into view
        # self.driver.execute_script("arguments[0].scrollIntoView(true);", slider)
        # time.sleep(1)  # 给浏览器时间渲染页面
        #
        # # 更新截图，包括缺失块
        # self.driver.save_screenshot("./huakuai/screenshot_updated.png")
        # # 裁剪并保存为真实尺寸的图片
        # image = Image.open("./huakuai/screenshot_updated.png")
        # box = (left, 0, left + width, image.size[1])
        # cropped_image = image.crop(box)
        # cropped_image.save("./huakuai/real_size_block.png")
        #
        # print("***************1", slider.size['width'])

        self.getImages()

        # # full bg
        # self.getCanvasImage(canvas_index=2)

        #
        # # Read the image from the specified path
        # im = cv2.imread('./huakuai/quanping.jpg')
        #
        # # Crop the image to the region of interest (ROI)
        # # Here, the ROI is defined from (12, 12) to (58, 58)
        # cropped_im = im[12:58, 12:58]
        #
        # # Display the cropped image (optional)
        # cv2.imshow('Cropped Image', cropped_im)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #
        # # Save the cropped image (optional)
        # cv2.imwrite('./huakuai/quekuai.jpg', cropped_im)

        # a = self.identify_gap("huakuai/bj.jpg", "huakuai/quekuai.jpg", "huakuai/out.jpg")

        distance = 0
        # distance = self.get_element_slide_distance("huakuai/quekuai_realsize.jpg", "huakuai/bg.jpg")
        distance = self.identify_gap("huakuai/bg.jpg", "huakuai/quekuai_realsize.jpg", "huakuai/out.jpg")
        if distance == 0:
            print("a的值为零，刷新再来一遍。。。")
            div_refresh = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.geetest_refresh_1")))
            div_refresh.click()
            time.sleep(3)
            self.getImages()
            distance = smzdm_obj.get_element_slide_distance("huakuai/quekuai_realsize.jpg", "huakuai/bg.jpg")

        print(distance, '........................')
        action = self.slide_slowly(slider, distance)

        try:
            # div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.geetest_panel_success")))

            # Define the locator for the element (e.g., using CSS_SELECTOR)
            element_locator = (By.CSS_SELECTOR, 'div.geetest_panel_success')
            # Define the text you are waiting for
            text_to_wait_for = '通过验证'

            # Initialize WebDriverWait with a timeout (e.g., 10 seconds)
            # wait = WebDriverWait(driver, 10)

            # Wait until the text is present in the specified element
            wait.until(EC.text_to_be_present_in_element(element_locator, text_to_wait_for))
            # div = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.geetest_panel_success")))
            print("validate successfully...")
        except Exception as e:
            print(str(e))
            try:
                # div_error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.geetest_panel_error")))
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.geetest_panel_error")))
                div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.geetest_panel_error_content")))
                div.click()
                time.sleep(2)
            except Exception as e:
                print(str(e))
                div_refresh = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.geetest_refresh_1")))
                div_refresh.click()
                time.sleep(3)
                self.getImages()
                distance = smzdm_obj.get_element_slide_distance("huakuai/quekuai_realsize.jpg", "huakuai/bg.jpg")

            self.slide_slowly2(slider, distance)
            time.sleep(5)

        # 切换回登录窗口
        self.driver.switch_to.window(self.driver.window_handles[0])
        # self.driver.find_element(By.XPATH, '//*[@id="index-head"]/div[3]/div[2]/a')
        button = self.driver.find_element(By.CSS_SELECTOR, "div.old-entry > a.J_punch")
        # print(button.text)
        if button.text.startswith("已"):
            print(button.text)
        else:
            button.click()

        # action.click_and_hold(slider).move_by_offset(a, 0).release().perform()

        # i = 0
        # # 执行滑动滑块的操作
        # action = ActionChains(self.driver)
        # action.click_and_hold(slider).perform()
        #
        # # 移动滑块到指定位置，这里以100像素为例
        # for i in range(50):
        #     action.move_by_offset(2, 0).perform()
        #     time.sleep(0.2)  # 暂停一段时间来模拟人的滑动动作
        #
        # # 释放滑块
        # action.release().perform()
        # time.sleep(10)  # 预留了安全验证的时间
        # # self.driver.refresh()  # 刷新页面

        self.driver.quit()

    def slide_slowly(self, element, distance):
        action = ActionChains(self.driver)
        # action.speed = 0.5
        # action.click_and_hold(slider).move_by_offset(a, 0).release().perform()
        action.click_and_hold(element).perform()
        # action.move_by_offset(a, 0).perform()
        # time.sleep(0.2)
        # 移动滑块到指定a位置
        for i in range(int(distance / 2)):
            action.move_by_offset(2, 0).perform()
            time.sleep(0.02)  # 暂停一段时间来模拟人的滑动动作
        # 释放滑块
        action.release().perform()
        time.sleep(3)
        return action

    def slide_slowly2(self, element, distance):
        """
        慢慢滑动滑块模拟人的操作，一次次移动一点点
        传入 浏览器对象、元素位置、移动距离 实现移动滑块
        :param driver: 浏览器对象
        :param element: 元素位置
        :param distance: 移动距离
        :return:
        """
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()
        # ActionChains(self.driver).click_and_hold(element).perform()
        # 移动小滑块，模拟人的操作，一次次移动一点点
        i = 0
        moved = 0
        while moved < distance:
            x = random.randint(3, 10)  # 每次移动3到10像素
            moved += x
            action.move_by_offset(xoffset=x, yoffset=0).perform()
            print("第{}次移动后，位置为{}".format(i, element.location['x']))
            time.sleep(0.02)  # 暂停一段时间来模拟人的滑动动作
            i += 1
        # 移动完之后，松开鼠标
        action.release().perform()

    def getImages(self):
        self.driver.save_screenshot("./huakuai/quanping.jpg")

        # bg without quekuai
        self.getCanvasImage(canvas_index=0)
        # quekuai
        self.getCanvasImage(canvas_index=1)
        # 裁剪图像
        cropped_image = self.crop_image('./huakuai/quekuai.jpg')
        # # 显示裁剪后的图像
        # cv2.imshow('Cropped Image', cropped_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite('./huakuai/quekuai_realsize.jpg', cropped_image)

    def getCanvasImage(self, canvas_index=0):
        try:
            # 执行 JavaScript 脚本，获取 Canvas 中的图片数据
            canvas_image_data = self.driver.execute_script(f"""
                var canvas = document.getElementsByTagName('canvas')[{canvas_index}];
                // 将 Canvas 导出为图像数据
                var imageData = canvas.toDataURL("image/png");

                // 返回图像数据
                return imageData;
            """, )

            # 解码图像数据
            image_data = base64.b64decode(canvas_image_data.split(",")[1])
            file_path = "huakuai/bg.jpg"
            if canvas_index == 1:
                file_path = "huakuai/quekuai.jpg"
            elif canvas_index == 2:
                file_path = "huakuai/fullbg.jpg"
            # 将图像数据保存到文件
            with open(file_path, "wb") as image_file:
                image_file.write(image_data)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def test_job(self):
        left1 = self.identify_gap("huakuai/bg.jpg", "huakuai/quekuai_realsize2.jpg", "huakuai/out.jpg")
        left2 = self.get_element_slide_distance("huakuai/quekuai_realsize2.jpg", "huakuai/bg.jpg")
        left3 = self.match("huakuai/bg.jpg", "huakuai/quekuai_realsize2.jpg")

        left4 = self.identify_gap("img/img_jd.jpg", "img/img_quekuai_jd.jpg", "img/out.jpg")
        left5 = self.get_element_slide_distance("img/img_quekuai_jd.png", "img/img_jd.jpg")
        left6 = self.match("img/img_jd.jpg", "img/img_quekuai_jd.jpg")
        print("方法identify_gap的返回值：", left1)
        print("方法get_element_slide_distance的返回值：", left2)
        print("方法match的返回值：", left3)
        #
        print(left1, left2, left3)
        #
        print("jd--方法identify_gap的返回值：", left4)
        print("jd--方法get_element_slide_distance的返回值：", left5)
        print("jd--方法match的返回值：", left6)
        print(left4, left5, left6)



if __name__ == '__main__':
    smzdm_obj = SMZDM()
    smzdm_obj.test_login()

    smzdm_obj.test_job()

    # # schedule.every().day.at("09:30").do(smzdm_obj.test_login())
    # schedule.every().day.at("18:32").do(smzdm_obj.test_job())
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
