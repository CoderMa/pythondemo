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

x_3 = range(1, 32)
x_10 = range(51, 82)
# y_3 = [22, 9, 15, 12, 13, 11, 9, 22, 23, 13, 19, 13, 19, 14, 21, 20, 20, 17, 19, 16, 9, 19, 17, 13, 19, 18, 14, 23, 16, 14, 15]
# y_10 = [29, 27, 27, 29, 28, 24, 23, 24, 28, 23, 25, 29, 24, 23, 26, 27, 26, 29, 27, 29, 23, 27, 27, 28, 25, 29, 24, 24, 25, 28, 29]
y_3 = [random.randint(9, 23) for i in range(31)]
y_10 = [random.randint(23, 29) for i in range(31)]

plt.scatter(x_3, y_3, label="3月份")
plt.scatter(x_10, y_10, label="10月份")

_x = list(x_3)+list(x_10)
_xticks_labels = ["3月{}日".format(i) for i in x_3]
_xticks_labels += ["10月{}日".format(i-50) for i in x_10]
plt.xticks(_x[::3], _xticks_labels[::3], rotation=45)

plt.xlabel("时间")
plt.ylabel("温度")
plt.title("测量数据")

plt.legend()

plt.show()
