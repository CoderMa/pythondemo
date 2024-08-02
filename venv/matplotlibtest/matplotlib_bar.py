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

# 设置图片大小
plt.figure(figsize=(20, 12), dpi=80)

x = np.array(["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"])
y = np.array([12, 22, 6, 18])

# 绘制柱形图
# plt.bar(x, y, color="#4CAF50")
# plt.bar(x, y, color=["#4CAF50", "red", "hotpink", "#556B2F"], width=0.5)   # width 控制线条的宽度
plt.barh(x, y, color=["#4CAF50", "red", "hotpink", "#556B2F"], height=0.5)   # height 控制线条的高低
plt.show()
