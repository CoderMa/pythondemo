import matplotlib.pyplot as plt
import numpy as np

# y = np.array([35, 25, 25, 15])
#
# plt.pie(y,
#         labels=['A', 'B', 'C', 'D'],  # 设置饼图标签
#         colors=["#d5695d", "#5d8ca8", "#65a479", "#a564c9"],  # 设置饼图颜色
#         )
# plt.title("RUNOOB Pie Test")  # 设置标题
# plt.show()


# # 数据
# sizes = [15, 30, 45, 10]
#
# # 饼图的标签
# labels = ['A', 'B', 'C', 'D']
#
# # 饼图的颜色
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
#
# # 突出显示第二个扇形, 值越大，距离中心越远
# explode = (0, 0.1, 0, 0)
#
# # 绘制饼图
# plt.pie(sizes, explode=explode, labels=labels, colors=colors,
#         autopct='%1.1f%%', shadow=True, startangle=90)
#
# # 标题
# plt.title("RUNOOB Pie Test")
#
# # 显示图形
# plt.show()


y = np.array([35, 25, 25, 15])

plt.pie(y,
        labels=['A', 'B', 'C', 'D'],  # 设置饼图标签
        colors=["#d5695d", "#5d8ca8", "#65a479", "#a564c9"],  # 设置饼图颜色
        explode=(0, 0.2, 0, 0),  # 第二部分突出显示，值越大，距离中心越远
        autopct='%.2f%%',  # 格式化输出百分比
        )
plt.title("RUNOOB Pie Test")
plt.show()
