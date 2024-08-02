from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import base64
import cv2


def identify_gap(bg, tp, out):
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
    print(tl[0])
    # 返回缺口的X坐标
    return tl[0]

# 启动浏览器
driver = webdriver.Chrome()

# 打开网页
driver.get("https://netc1.igtb.bankofchina.com/#/login-page")
driver.maximize_window()
time.sleep(5)
# 定位滑块元素
slider = driver.find_element(By.XPATH,
                             '/html/body/div[1]/div/div[2]/div/div/form/div[5]/div/div/div/div/div[2]/div[2]/div[2]/div[1]')  # 替换为实际的滑块元素的ID

image_url = driver.find_element(By.CSS_SELECTOR, '#dx_captcha_basic_sub-slider_2 > img').get_attribute("src")
print(image_url)
img_element = driver.find_element(By.CSS_SELECTOR, '#dx_captcha_basic_sub-slider_2 > img')
parent_element = driver.find_element(By.CSS_SELECTOR, '#dx_captcha_basic_sub-slider_2')
original_style = img_element.get_attribute('style')

image_selector = "#dx_captcha_basic_sub-slider_2 > img"
# 使用 JavaScript 修改图片元素的样式，将其显示出来
show_image_script = f'''
    var img = document.querySelector("{image_selector}");
    img.style.position = "absolute";
    img.style.left = "10px";  // 替换为你想要的横坐标
    img.style.top = "10px";    // 替换为你想要的纵坐标
    document.body.appendChild(img);  // 将图片移动到 body 元素下

'''
driver.execute_script(show_image_script)
driver.save_screenshot("D:/quanping.png")
time.sleep(5)
driver.execute_script(f'arguments[0].style = "{original_style}";', img_element)
driver.execute_script("arguments[1].appendChild(arguments[0]);", img_element, parent_element)

time.sleep(2)
try:
    # 执行 JavaScript 脚本，获取 Canvas 中的图片数据

    canvas_image_data = driver.execute_script("""
        var canvas = document.getElementsByTagName('canvas')[0];
        // 将 Canvas 导出为图像数据
        var imageData = canvas.toDataURL("image/png");

        // 返回图像数据
        return imageData;
    """, )

    # 解码图像数据
    image_data = base64.b64decode(canvas_image_data.split(",")[1])
    # 将图像数据保存到文件
    with open("huakuai/bj.png", "wb") as image_file:
        image_file.write(image_data)


except Exception as e:
    print(f"An error occurred: {str(e)}")

im = cv2.imread('D:/quanping.png')
im = im[12:58, 12:58]
cv2.imwrite('huakuai/quekuai.png', im)
a = identify_gap("huakuai/bj.png", "huakuai/quekuai.png", "huakuai/out.png")

action = ActionChains(driver)
# action.click_and_hold(slider).move_by_offset(a, 0).release().perform()
i = 0
print(a)
action.speed = 0.5
action.click_and_hold(slider).move_by_offset(a, 0).release().perform()
time.sleep(20)
driver.quit()
