import time
import unittest
# from HwTestReport import HTMLTestReport
# from HwTestReport import HTMLTestReportEN
import requests
from requests.cookies import cookiejar_from_dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import HTMLTestRunner
from common import logger


class Case_baidu(unittest.TestCase):
    """
    在python3中因为unittest运行机制变动，在使用setUp/tearDown中初始化/退出driver时，可能会出现用例执行失败没有截图的问题，但我没有遇到过，如果出现请使用setUpClass/tearDownClass的用法
    """

    log = logger.Log()

    def setUp(self):
        self.imgs = []
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def tearDown(self):
        print("imgs 的长度为：", len(self.imgs))
        self.driver.quit()

    def get_screenshot(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        self.imgs.append(self.driver.save_screenshot('./%s.png' % str(time.time())))
        return True

    def test_baidu_search(self):
        """用例通过，没有报告内容，有多张截图"""
        self.log.info("--------start testing baidu search!---------")
        self.driver.get("https://www.baidu.com")
        self.get_screenshot()
        self.driver.find_element(By.ID, 'kw').send_keys('Python')
        self.get_screenshot()
        self.driver.find_element(By.ID, 'su').click()
        time.sleep(3)
        self.get_screenshot()
        self.log.info("--------end!---------")

    def test_baidu_assert_ok(self):
        """用例通过，有报告内容，有截图"""
        self.log.info("--------start testing test_baidu_assert_ok !---------")
        self.driver.get("https://www.baidu.com")
        hao123 = self.driver.find_element(By.XPATH, '//*[@id="u1"]/a[2]').text
        print(hao123)
        self.log.info(hao123)
        self.get_screenshot()
        self.assertEqual(hao123, 'hao123')
        self.log.info("--------end!---------")

    def test_baidu_assert_ok_noimg(self):
        """用例通过，有报告内容，没有截图"""
        self.driver.get("https://www.baidu.com")
        news = self.driver.find_element(By.XPATH, '//*[@id="u1"]/a[1]').text
        print(news)
        self.assertEqual(news, "新闻")

    def test_baidu_assert_faile(self):
        """用例失败，带有失败内容和截图"""
        self.driver.get("https://www.baidu.com")
        self.get_screenshot()
        news = self.driver.find_element(By.XPATH, '//*[@id="u1"]/a[1]').text
        print(news)
        self.get_screenshot()
        self.driver.find_element(By.XPATH, '//*[@id="u1"]/a[1]').click()
        self.get_screenshot()
        self.assertEqual(news, 'hao123')

    def test_baidu_assert_error(self):
        """用例错误，带有指定错误内容和截图"""
        self.driver.get("https://www.baidu.com")
        self.get_screenshot()
        raise EnvironmentError('Current environment can not testing!')


class Case_qq(unittest.TestCase):
    def setUp(self):
        self.imgs = []
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_qq_index_faile(self):
        """用例错误，带有错误内容和没有截图"""
        self.driver.get("https://www.qq.com")
        self.driver.find_element(By.ID, 'sougouTxt').send_keys('搜狗搜索')
        # self.driver.find_element_by_id('sougouTxt').send_keys('搜狗搜索')
        self.driver.find_element(By.ID, 'searchBtn').click()
        self.assertIn(u"搜狗", u'搜索')

    def test_qq_index_ok(self):
        """用例通过，没有内容和没有截图"""
        self.driver.get("https://www.qq.com")
        self.driver.find_element(By.ID, 'sougouTxt').send_keys('搜狗搜索')
        self.driver.find_element(By.ID, 'searchBtn').click()


class Case_163(unittest.TestCase):
    def setUp(self):
        self.imgs = []
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_163_ok(self):
        """通过 没有内容和截图"""
        self.driver.get("https://www.163.com/")


def cookie_info(login_url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")

    # login_url = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.jianhua.201864-2.d1.5af911d9lhGWni&f=top&redirectURL=http%3A%2F%2Fwww.taobao.com%2F'
    driver = webdriver.Chrome(options=chrome_options)
    print("请尽快扫码！")
    driver.get(login_url)
    time.sleep(15)  # 预留了安全验证的时间
    driver.refresh()  # 刷新页面
    c = driver.get_cookies()
    sessions = dict()
    for cookie in c:
        sessions[cookie['name']] = cookie['value']
    # driver.quit()
    return sessions


class Case_smzd(unittest.TestCase):
    def setUp(self):
        self.imgs = []
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        # login_url = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.jianhua.201864-2.d1.5af911d9lhGWni&f=top&redirectURL=http%3A%2F%2Fwww.taobao.com%2F'
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        """通过 没有内容和截图"""
        # self.driver.get("https://www.smzdm.com/")
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

        self.driver.find_element(By.ID, "username").send_keys("mjlei007@163.com")
        time.sleep(1)
        self.driver.find_element(By.ID, "password").send_keys("mjlei!@0051")
        time.sleep(1)
        self.driver.find_element(By.ID, "loginAgreement").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "login_submit").click()

        # self.driver.switch_to.frame('J_login_iframe')
        windows = self.driver.window_handles  # 所有窗口句柄
        # 切换到验证窗口
        self.driver.switch_to.window(windows[-1])
        # 找到滑块元素
        slider = self.driver.find_element(By.CLASS_NAME, 'geetest_slider_button')
        sleder2 = self.driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div[6]/div/div[1]/div[2]/div[2]')

        # 执行滑动滑块的操作
        ActionChains(self.driver).click_and_hold(slider).perform()

        # 移动滑块到指定位置，这里以100像素为例
        for i in range(100):
            ActionChains(self.driver).move_by_offset(2, 0).perform()
            time.sleep(0.2)  # 暂停一段时间来模拟人的滑动动作

        # 释放滑块
        ActionChains(self.driver).release().perform()
        # time.sleep(15)  # 预留了安全验证的时间
        # self.driver.refresh()  # 刷新页面

        print("test.....")
        time.sleep(5)

        # 切换回登录窗口
        self.driver.switch_to.window(windows[0])
        self.driver.find_element(By.XPATH, '//*[@id="index-head"]/div[3]/div[2]/a')
        time.sleep(15)


if __name__ == "__main__":
    # suite1 = unittest.TestLoader().loadTestsFromTestCase(Case_baidu)
    # suite2 = unittest.TestLoader().loadTestsFromTestCase(Case_qq)
    # suite3 = unittest.TestLoader().loadTestsFromTestCase(Case_163)

    suite4 = unittest.TestLoader().loadTestsFromTestCase(Case_baidu)
    suites = unittest.TestSuite()
    # suites.addTests([suite1, suite2, suite3])
    suites.addTests([suite4])

    # HTMLTestReport or HTMLTestReportEN
    with open('./HwTestReportIMG.html', 'wb') as report:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report,
                                               verbosity=2,
                                               title='HwTestReport 测试',
                                               description='带截图，带饼图，带详情')
        runner.run(suites)
