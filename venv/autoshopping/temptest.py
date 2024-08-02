import re
import time
import cv2

def test_regex():
    base64_str = "data:image/png;base64,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"
    # pattern = "^data:image/png;base64,(.*?)"
    pattern = r"^data:image/\w+;base64,(.+)"
    image_str = re.findall(pattern, base64_str, re.S)  # re.S表示点号匹配任意字符，包括换行符
    print(image_str)

def get_pos(img1, num, num1, num2, diff_pixel1=4, diff_pixel2=4):
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
        if num * num - num * num / diff_pixel1 < area < num * num + num * num / diff_pixel1 and num * diff_pixel1 - num * diff_pixel1 / diff_pixel1 < length < num * diff_pixel1 + num * diff_pixel1 / diff_pixel1:
            # 计算轮廓的边界矩形，得到坐标和宽高
            # x, y: 边界矩形左上角点的坐标。
            # w, h: 边界矩形的宽度和高度。
            x, y, w, h = cv2.boundingRect(contour)
            print("计算出目标区域的坐标及宽高：", x, y, w, h)
            # 在目标区域上画一个红框看看效果
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imwrite("img/test.jpg", image)
            return x * num1 / num2 - diff_pixel2
    return 0

def test2():
    # 2、图片位置（相对当前项目）
    img = 'img/img1.jpg'
    # 3、缺口像素长宽（长宽必须一致）
    gap_wide = 80
    # 4、web图片宽度
    web_wide = 340
    # 5、原图片宽度
    raw_wide = 672
    # 调用方法获取返回的移动距离
    dis = get_pos(img, gap_wide, web_wide, raw_wide)
    # 打印一下移动距离
    print("dis=", dis)

def test_jd():
    # 2、图片位置（相对当前项目）
    img = 'img/img_jd.png'
    # 3、缺口像素长宽（长宽必须一致）
    gap_wide = 50
    # 4、web图片宽度
    web_wide = 360
    # 5、原图片宽度
    raw_wide = 360
    # 调用方法获取返回的移动距离
    dis = get_pos(img, gap_wide, web_wide, raw_wide, 1, 1)
    # 打印一下移动距离
    print("dis=", dis)

if __name__ == '__main__':
    # # 2、图片位置（相对当前项目）
    # img = "huakuai/bg.jpg"
    # # 3、缺口像素长宽（长宽必须一致）
    # gap_wide = 60
    # # 4、web图片宽度
    # web_wide = 260
    # # 5、原图片宽度
    # raw_wide = 260
    # # 调用方法获取返回的移动距离
    # dis = get_pos(img, gap_wide, web_wide, raw_wide, 1, 0)
    # # 打印一下移动距离
    # print("dis=", dis)
    # print("time sleep 5 seconds.....")
    # time.sleep(5)
    # print("test2")
    # test2()
    # print("test jd")
    # test_jd()
    #
    #
    test_regex()
