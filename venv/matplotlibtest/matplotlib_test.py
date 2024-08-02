import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
from matplotlib import font_manager

# matplotlib.use('Qt5Agg')
print(matplotlib._get_version())

# # windows和Linux设置字体的方法
font = {'family': 'MicroSoft YaHei',
        'weight': 'bold',
        'size': 14}
# 方法1
matplotlib.rc('font', **font)
# 方法2
# matplotlib.rc('font', family='Microsoft YaHei', weight='bold')

# 方法3
# my_font = font_manager.FontProperties(fname='./msyh.ttc')



# # 通过两个坐标 (0,0) 到 (6,100) 来绘制一条线:
# xpoints = np.array([0, 6])
# ypoints = np.array([0, 100])
#
# plt.plot(xpoints, ypoints)
# plt.show()

# x = np.linspace(0, 2 * np.pi, 200)
# y = np.sin(x)
#
# fig, ax = plt.subplots()
# ax.plot(x, y)
# plt.show()


# fig, ax = plt.subplots()
#
# fruits = ['apple', 'blueberry', 'cherry', 'orange']
# counts = [40, 100, 30, 55]
# bar_labels = ['red', 'blue', '_red', 'orange']
# bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']
#
# ax.bar(fruits, counts, label=bar_labels, color=bar_colors)
#
# ax.set_ylabel('fruit supply')
# ax.set_title('Fruit supply by kind and color')
# ax.legend(title='Fruit color')
#
# plt.show()


"""
# x = [1, 2, 3, 4, 5]
x = range(2, 28, 2)
y = [15, 13, 14, 5, 17, 20, 25, 26, 26, 27, 22, 18, 15]

# 设置图片大小
plt.figure(figsize=(20, 8), dpi=80)

# 绘图
plt.plot(x, y)

# 设置x轴刻度
xtick_labels = [i/2 for i in range(4, 49)]
# print(xtick_labels)
# plt.xticks(range(25, 50))
plt.xticks(xtick_labels)
plt.yticks(range(min(y), max(y)+1))
#
# # 保存图片
# plt.savefig('./plt1.png')
plt.show()

"""

x = range(0, 120)
y1 = [random.randint(20, 35) for i in range(120)]
y2 = [random.randint(20, 35) for i in range(120)]
print("y1: ", y1)
print("y2: ", y2)

# 设置图片大小
plt.figure(figsize=(20, 12), dpi=80)

# 绘图
# plt.plot(x, y1)
# plt.plot(x, y2)
# plt.plot(x, y1, label='第一条')
plt.plot(x, y1, label='第一条', color='orange', linestyle='--')
plt.plot(x, y2, label='第二条', color='cyan', linestyle=':')

# 调整x轴刻度
# _x = x
# _x = list(x)[::3]
_x = list(x)
# _xtick_lables = ["hello {}".format(i) for i in _x]
_xtick_lables = ["10点 {}分".format(i) for i in range(60)]
_xtick_lables += ["11点 {}分".format(i) for i in range(60)]
# 取步长， 数字和字符串一一对应， 数据的长度一样
# plt.xticks(_x[::3], _xtick_lables[::3])
plt.xticks(_x[::3], _xtick_lables[::3], rotation=45)  # rotation旋转度数
# plt.xticks(_x[::3], _xtick_lables[::3], rotation=45, fontproperties=my_font)  # rotation旋转度数, fontproperties字体

# # 保存图片
plt.savefig('./plt1.png')

# 添加描述信息
plt.xlabel("时间")
plt.ylabel("温度 单位摄氏度")
plt.title("10点到12点每分钟的气温变化情况")

# 绘制网格
plt.grid(alpha=0.4, linestyle=':')

# 添加图例
plt.legend(loc=0)
# plt.legend(loc='best')
# plt.legend(loc='upper right')
# plt.legend(prop=my_font)

plt.show()
