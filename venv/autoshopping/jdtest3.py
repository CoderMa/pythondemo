from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import webbrowser, base64, io

from PIL import Image
import random
import cv2
import pyautogui
import time
import webbrowser
import requests, json, re
import time
import random
import shutil
import pyperclip
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import keyboard, os, uuid
from PIL import ImageGrab

from YdmVerify import YdmVerify

y = YdmVerify()
##author:byc6352
##technical support:byc6352 or metabycf or 39848872
card_id = '55ADCB28DBC56EB4'
url = "https://mygiftcard.jd.com/giftcard/myGiftCardInit.action"


def login(driver, cookies=''):
    ##自动登录
    driver.get('https://www.jd.com/')
    driver.switch_to.window(driver.window_handles[-1])
    driver.maximize_window()
    driver.delete_all_cookies()
    if cookies == '':
        cookies = [
            {'domain': '.jd.com', 'expiry': 1717384813, 'httpOnly': False, 'name': '__jdb', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': '76161171.5.1717382950957103922947|1.1717382951'},
            {'domain': '.jd.com', 'expiry': 1732935013, 'httpOnly': False, 'name': '__jda', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': '76161171.1717382950957103922947.1717382951.1717382951.1717382951.1'},
            {'domain': '.jd.com', 'httpOnly': False, 'name': '__jdc', 'path': '/', 'sameSite': 'Lax', 'secure': False,
             'value': '76161171'},
            {'domain': '.jd.com', 'expiry': 1748918985, 'httpOnly': False, 'name': 'pinId', 'path': '/',
             'sameSite': 'None',
             'secure': True, 'value': 'YCe8rw2G6w2zBk65PfDfDg'},
            {'domain': '.jd.com', 'expiry': 1719974985, 'httpOnly': False, 'name': 'pin', 'path': '/',
             'sameSite': 'None',
             'secure': True, 'value': 'jd_XLCuliLsIoml'},
            {'domain': '.jd.com', 'expiry': 1717386601, 'httpOnly': False, 'name': 'jsavif', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': '1'},
            {'domain': '.jd.com', 'expiry': 1717384801, 'httpOnly': False, 'name': 'token', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': '58b2853fe33d43b6606c5a21df75d6e5,3,954101'},
            {'domain': '.jd.com', 'expiry': 1719975003, 'httpOnly': False, 'name': 'ipLoc-djd', 'path': '/',
             'sameSite': 'Lax', 'secure': False, 'value': '25-2258-2261-6568'},
            {'domain': 'www.jd.com', 'expiry': 1717386590, 'httpOnly': False, 'name': 'UseCorpPin', 'path': '/',
             'sameSite': 'Lax', 'secure': False, 'value': 'jd_XLCuliLsIoml'},
            {'domain': '.jd.com', 'expiry': 1719974985, 'httpOnly': False, 'name': '_tp', 'path': '/',
             'sameSite': 'None',
             'secure': True, 'value': 'gcPCiSoOxTEQh1UmLWSJmA%3D%3D'},
            {'domain': '.jd.com', 'expiry': 1718246952, 'httpOnly': False, 'name': 'areaId', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': '25'},
            {'domain': '.jd.com', 'expiry': 1719974985, 'httpOnly': False, 'name': 'unick', 'path': '/',
             'sameSite': 'None',
             'secure': True, 'value': '717tjgq12eb3u3'},
            {'domain': '.jd.com', 'expiry': 1717383072, 'httpOnly': False, 'name': '_gia_d', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': '1'},
            {'domain': '.jd.com', 'expiry': 1751942985, 'httpOnly': False, 'name': 'TrackID', 'path': '/',
             'sameSite': 'None', 'secure': True,
             'value': '16Qvq9anbTkSX8gr4zaukUq5uQYslojZC9OQmewQghRGZ3XvjG_MMnzr_vyEIKSdUCtJ2wRpSFTY3eQtR-mtgEtTLaduuEqMy1V9rbOxT2sDX0aNazsKZ9ymfF8kbb66r'},
            {'domain': '.jd.com', 'expiry': 1751943003, 'httpOnly': False, 'name': 'shshshfpb', 'path': '/',
             'sameSite': 'Lax', 'secure': False, 'value': 'BApXcwpUJ3-pAgpgn7ERHMlecUhcGxJTHBlV5Lnto9xJ1MukUQIC2'},
            {'domain': '.jd.com', 'expiry': 1751943002, 'httpOnly': False, 'name': 'shshshfpa', 'path': '/',
             'sameSite': 'Lax', 'secure': False, 'value': '52743637-1e03-a986-e555-3b60bd02251d-1717382954'},
            {'domain': '.jd.com', 'expiry': 1751942954, 'httpOnly': False, 'name': 'shshshfpx', 'path': '/',
             'sameSite': 'Lax', 'secure': False, 'value': '52743637-1e03-a986-e555-3b60bd02251d-1717382954'},
            {'domain': 'www.jd.com', 'expiry': 1748918953, 'httpOnly': False, 'name': 'o2State', 'path': '/',
             'sameSite': 'Lax', 'secure': False,
             'value': '{%22webp%22:true%2C%22avif%22:true%2C%22lastvisit%22:1717382953020}'},
            {'domain': '.jd.com', 'expiry': 1718678985, 'httpOnly': True, 'name': 'thor', 'path': '/',
             'sameSite': 'None',
             'secure': True,
             'value': 'B4C20964EEB81D93A1282B10D740DDCE93E6BF376C1A027834CA7420581040CA1F1691CE77DF8E8D4839BB18578D59CADD7B65F3464D14E69D56C466193409E2C5CC1CCC0FB0077D600F5E5A9050977080A6CD9DB54BF53D86A4A33D85C531B9CBA745CE208771BE1D5DFCEBADFD8E0CEB8C892454D65E7595BB979BE56296A5F7B62DAF0FD0D84D7FE1241F16E5B46A7A60AB7C12103EA76433421EA1F54E0A'},
            {'domain': '.jd.com', 'expiry': 1743302958, 'httpOnly': False, 'name': '3AB9D23F7A4B3C9B', 'path': '/',
             'sameSite': 'Lax', 'secure': False,
             'value': 'IGRRJT2FGAUX2L3XBSLXZRHOWGH7YNRHMBQHXA7OMUM75D6BQNTIV6YWQQLNKHV2URUHMEDS7BVALS47ABD56MW5TA'},
            {'domain': '.jd.com', 'expiry': 1718679002, 'httpOnly': True, 'name': 'flash', 'path': '/',
             'sameSite': 'None',
             'secure': True,
             'value': '2_zpZqs4H7M7_a9OhxVV4eMXgMPNf1o8Lxl-gS2Cneh79n2xY8IA6o9y5JglFeAKaQiZht9zwAUXVJco4lj9A4vcdvIQiBDvy8LbsO_AFm1vttvRjlsuRLrbjHGIQSlouU9NJknNKUB8TbCWUlqFfY8wD2CdBj94DPObXyoggI_DK*'},
            {'domain': '.jd.com', 'expiry': 1719974985, 'httpOnly': True, 'name': '_pst', 'path': '/',
             'sameSite': 'None',
             'secure': True, 'value': 'jd_XLCuliLsIoml'},
            {'domain': '.jd.com', 'expiry': 1717384801, 'httpOnly': False, 'name': '__tk', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': 'VnTIiUTISDSEikqDVAvHVAvJTLe5Wne3iLTHiUSFikuATcVIVkq3i2,3,954101'},
            {'domain': '.jd.com', 'expiry': 1748486952, 'httpOnly': False, 'name': '3AB9D23F7A4B3CSS', 'path': '/',
             'sameSite': 'Lax', 'secure': False,
             'value': 'jdd03IGRRJT2FGAUX2L3XBSLXZRHOWGH7YNRHMBQHXA7OMUM75D6BQNTIV6YWQQLNKHV2URUHMEDS7BVALS47ABD56MW5TAAAAAMP3QADWNQAAAAACGG4IYVAGJI3JMX'},
            {'domain': '.jd.com', 'expiry': 1732935018, 'httpOnly': False, 'name': '__jdu', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': '1717382950957103922947'},
            {'domain': '.jd.com', 'httpOnly': False, 'name': 'ceshi3.com', 'path': '/', 'sameSite': 'None',
             'secure': True,
             'value': '000'},
            {'domain': '.jd.com', 'expiry': 1718678950, 'httpOnly': False, 'name': '__jdv', 'path': '/',
             'sameSite': 'Lax',
             'secure': False, 'value': '76161171|direct|-|none|-|1717382950958'}]
    for cookie in cookies:
        driver.add_cookie(cookie)
    ##driver.refresh()
    driver.get(url)


def click_verify():
    # 图标点选
    try:
        ## 截图保存
        img = ImageGrab.grab(bbox=(759, 421, 1141, 793))
        img.save('./sel.jpg')
        with open(r'./sel.jpg', 'rb') as f:
            im = f.read()
        ## 图像识别
        ret = y.click_verify(image=im, verify_type="30330")
        print("ret=" + ret)
        ret = str(ret)
        pos = ret.split(',')
        pos[0] = int(pos[0])
        pos[1] = int(pos[1])
        # 移动鼠标到起始位置
        pyautogui.moveTo(pos[0] + 759, pos[1] + 421, duration=0.3)
        # 按下鼠标左键
        pyautogui.mouseDown()
        # 松开鼠标左键
        pyautogui.mouseUp()

        time.sleep(2)
        ## 失败 再次点选
        click_verify()
        return True
    except Exception as e:
        print('click_verify err:', e)
        return False


def slide_verify():
    ## 滑块验证
    try:
        ele_big = driver.find_element(By.ID, "cpc_img")
        ele_small = driver.find_element(By.ID, "small_img")

        src_big = ele_big.get_attribute('src')
        # print(src_big)
        src_small = ele_small.get_attribute('src')
        # 获取标准的base64字符串
        base64_big = src_big[22:]
        base64_small = src_small[22:]

        lo_small = [804, 753]
        ## 计算缺口滑块距离
        ret = y.slide_verify(base64_small, base64_big)
        ret = int(ret) + 30
        print(ret)
        ## 鼠标操作
        slide_mouse(lo_small, ret)
        return True
    except Exception as e:
        print('card_slide err:', e)
        ## 转到点选验证
        ret = click_verify()
        if ret == True:
            return True
        else:
            return False
        return False


def slide_mouse(pos, distance):
    ##滑块验证 移动鼠标

    start_x = pos[0]
    start_y = pos[1]
    end_x = pos[0] + distance
    end_y = pos[1]
    # 移动鼠标到起始位置
    pyautogui.moveTo(start_x, start_y, duration=0.3)
    # 按下鼠标左键
    pyautogui.mouseDown()
    # 往右多拖到20xp
    pyautogui.moveTo(end_x - 20, end_y - 20, duration=0.4)
    # 拖回结束位置
    pyautogui.moveTo(end_x, end_y, duration=0.5)
    # 松开鼠标左键
    pyautogui.mouseUp()


if __name__ == '__main__':
    ##chromedriver.exe 位置：C:\Users\Administrator\AppData\Local\Programs\Python\Python311
    driver = webdriver.Chrome()
    login(driver)
    time.sleep(5)
    ##自动输入卡号
    driver.find_element(By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/input').send_keys(
        card_id)
    ##点击按钮
    driver.execute_script(
        'document.querySelector("#root > div:nth-child(1) > div > div > div > div > div.bind-card > div.bind-form.clearfix > div:nth-child(3) > div").click()')

    time.sleep(3)
    # 滑块验证、点选验证
    for index in range(100):
        print('滑块验证，执行第： ', index)
        if not slide_verify(): break
        time.sleep(3)

    time.sleep(10)
