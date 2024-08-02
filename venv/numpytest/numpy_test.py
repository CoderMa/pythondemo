# from numpy import *
import numpy as np

"""
# print(np.eye(4))
a = np.array([1, 2, 3])
print(a)

b = np.array([[1, 2, 3], [4, 5, 6]])
print(b)

c = np.array([1, 2, 3, 4, 5], ndmin=3)
print(c)

d = np.array([1, 2, 3], dtype=complex)
print(d)

dt = np.dtype(np.int32)
print(dt)
print(type(dt))

# int8, int16, int32, int64 四种数据类型可以使用字符串 'i1', 'i2','i4','i8' 代替
dt = np.dtype('i4')
print(dt)
print(type(dt))

# 字节顺序标注
dt = np.dtype('<i4')
print(dt)

# 首先创建结构化数据类型
dt = np.dtype([('age', np.int8)])
print(dt)

# 将数据类型应用于 ndarray 对象
dt = np.dtype([('age', np.int8)])
a = np.array([(10,), (20,), (30,)], dtype=dt)
print(a)
# 类型字段名可以用于存取实际的 age 列
print(a['age'])

# 定义一个结构化数据类型 student，包含字符串字段 name，整数字段 age，及浮点字段 marks，并将这个 dtype 应用到 ndarray 对象。
student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])
print(student)
a = np.array([('abc', 21, 50), ('xyz', 18, 75)], dtype=student)
print(a)
"""

a = np.arange(24)
print(a)
print(a.ndim)  # a 现只有一个维度
# 现在调整其大小
b = a.reshape(2, 4, 3)  # b 现在拥有三个维度
print(b)
print(b.ndim)

# ndarray.shape 表示数组的维度，返回一个元组，这个元组的长度就是维度的数目，即 ndim 属性(秩)。比如，一个二维数组，其维度表示"行数"和"列数"。
c = np.array([[1, 2, 3], [4, 5, 6]])
print(c.shape)

# ndarray.shape 也可以用于调整数组大小
c.shape = (3, 2)
print(c)

# ndarray.itemsize 以字节的形式返回数组中每一个元素的大小。
# 数组的 dtype 为 int8（一个字节）
x = np.array([1, 2, 3, 4, 5], dtype=np.int8)
print(x.itemsize)

# 数组的 dtype 现在为 float64（八个字节）
y = np.array([1, 2, 3, 4, 5], dtype=np.float64)
print(y.itemsize)

# ndarray.flags 返回 ndarray 对象的内存信息
x = np.array([1, 2, 3, 4, 5])
print(x.flags)

# 创建空数组
# 注意 − 数组元素为随机值，因为它们未初始化。
x = np.empty([3, 2], dtype=int)
print(x)

# numpy.zeros
# 创建指定大小的数组，数组元素以 0 来填充：

# 默认为浮点数
x = np.zeros(5)
print(x)
# 设置类型为整数
y = np.zeros((5,), dtype=int)
print(y)
# 自定义类型
z = np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'i4')])
print(z)

# numpy.ones
# 创建指定形状的数组，数组元素以 1 来填充：
# 默认为浮点数
x = np.ones(5)
print(x)

# 自定义类型
x = np.ones([2, 2], dtype=int)
print(x)

# numpy.zeros_like
# numpy.zeros_like 用于创建一个与给定数组具有相同形状的数组，数组元素以 0 来填充。
# numpy.zeros 和 numpy.zeros_like 都是用于创建一个指定形状的数组，其中所有元素都是 0。
# 它们之间的区别在于：numpy.zeros 可以直接指定要创建的数组的形状，而 numpy.zeros_like 则是创建一个与给定数组具有相同形状的数组。

# 创建一个与 arr 形状相同的，所有元素都为 0 的数组：
# 创建一个 3x3 的二维数组
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# 创建一个与 arr 形状相同的，所有元素都为 0 的数组
zeros_arr = np.zeros_like(arr)
print(zeros_arr)

# numpy.ones_like
# numpy.ones_like 用于创建一个与给定数组具有相同形状的数组，数组元素以 1 来填充。
# numpy.ones 和 numpy.ones_like 都是用于创建一个指定形状的数组，其中所有元素都是 1。
# 它们之间的区别在于：numpy.ones 可以直接指定要创建的数组的形状，而 numpy.ones_like 则是创建一个与给定数组具有相同形状的数组。

# 创建一个与 arr 形状相同的，所有元素都为 1 的数组：
# 创建一个 3x3 的二维数组
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# 创建一个与 arr 形状相同的，所有元素都为 1 的数组
ones_arr = np.ones_like(arr)
print(ones_arr)

# NumPy 从已有的数组创建数组
# 将列表转换为 ndarray:
x = [1, 2, 3]
a = np.asarray(x)
print(a)
a = np.asarray(x, dtype=float)
print(a)

# 将元组列表转换为 ndarray:
x = [(1, 2, 3), (4, 5, 6)]
a = np.asarray(x)
print(a)

# numpy.frombuffer
# numpy.frombuffer 用于实现动态数组。
# numpy.frombuffer 接受 buffer 输入参数，以流的形式读入转化成 ndarray 对象。
# 注意：buffer 是字符串的时候，Python3 默认 str 是 Unicode 类型，所以要转成 bytestring 在原 str 前加上 b。
s = b'Hello World'
# s = 'Hello World'.encode(encoding='utf-8')
a = np.frombuffer(s, dtype='S1')
print(a)

# numpy.fromiter
# numpy.fromiter 方法从可迭代对象中建立 ndarray 对象，返回一维数组。
# 使用 range 函数创建列表对象
list = range(5)
print(type(list))
print(list)
it = iter(list)
print(type(it))
print(it)
# 使用迭代器创建 ndarray
x = np.fromiter(it, dtype=float)
print(x)

# NumPy 从数值范围创建数组
# numpy.arange
# numpy 包中的使用 arange 函数创建数值范围并返回 ndarray 对象
# 生成 0 到 4 长度为 5 的数组:
x = np.arange(5)
print(x)
# 设置了 dtype, 设置返回类型位 float:
x = np.arange(5, dtype=float)
print(x)
# 设置了起始值、终止值及步长：
x = np.arange(10, 20, 2)
print(x)

# numpy.linspace
# numpy.linspace 函数用于创建一个一维数组，数组是一个等差数列构成的
# 设置起始点为 1 ，终止点为 10，数列个数为 10。
a = np.linspace(1, 10, 10)
print(a)

# 设置元素全部是1的等差数列：
a = np.linspace(1, 1, 10)
print(a)

# 将 endpoint 设为 false，不包含终止值：
a = np.linspace(10, 20, 5, endpoint=False)
print(a)

# 将 endpoint 设为  设为 true，则会包含 终止值：
a = np.linspace(10, 20, 5, endpoint=True)
print(a)

# 设置间距。
a = np.linspace(1, 10, 10, retstep=True)
print(a)
# 拓展例子
b = np.linspace(1, 10, 10).reshape([10, 1])
print(b)

# numpy.logspace
# numpy.logspace 函数用于创建一个于等比数列。格式如下：
# np.logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None)
# start参数序列的起始值为：base ** start
# stop参数序列的终止值为：base ** stop。如果endpoint为true，该值包含于数列中
# base 参数意思是取对数的时候 log 的下标。
# 默认底数是 10
a = np.logspace(1.0, 2.0, num=10)
print(a)

# 将对数的底数设置为 2
a = np.logspace(0, 9, 10, base=2)
print(a)  # [  1.   2.   4.   8.  16.  32.  64. 128. 256. 512.]

# NumPy 切片和索引
a = np.arange(10)
print(a)
s = slice(2, 7, 2)  # 从索引 2 开始到索引 7 停止，间隔为2
print(a[s])
print(a[slice(2, 9, 2)])  # 从索引 2 开始到索引 9 停止，间隔为2
# 也可以通过冒号分隔切片参数 start:stop:step 来进行切片操作：
# 冒号 : 的解释：如果只放置一个参数，如 [2]，将返回与该索引相对应的单个元素。如果为 [2:]，表示从该索引开始以后的所有项都将被提取。如果使用了两个参数，如 [2:7]，那么则提取两个索引(不包括停止索引)之间的项。
b = a[2:7:2]  # 从索引 2 开始到索引 7 停止，间隔为 2
print(b)

a = np.arange(10)  # [0 1 2 3 4 5 6 7 8 9]
b = a[5]
print(b)

a = np.arange(10)
print(a[2:])

a = np.arange(10)  # [0 1 2 3 4 5 6 7 8 9]
print(a[2:5])

# 多维数组同样适用上述索引提取方法：
a = np.array([[1, 2, 3], [3, 4, 5], [4, 5, 6]])
print(a)
# 从某个索引处开始切割
print('从数组索引 a[1:] 处开始切割')
print(a[1:])

# 切片还可以包括省略号 …，来使选择元组的长度与数组的维度相同。
# 如果在行位置使用省略号，它将返回包含行中元素的 ndarray。
a = np.array([[1, 2, 3], [3, 4, 5], [4, 5, 6]])
print(a)
print("第2列元素", a[..., 1])  # 索引为1的列元素即第2列元素
print("第2行元素", a[1, ...])  # 第2行元素
print("第2列及剩下的所有元素:", a[..., 1:])  # 第2列及剩下的所有元素

# 整数数组索引
# 整数数组索引是指使用一个数组来访问另一个数组的元素。这个数组中的每个元素都是目标数组中某个维度上的索引值。
# 以下实例获取数组中 (0,0)，(1,1) 和 (2,0) 位置处的元素。
x = np.array([[1, 2], [3, 4], [5, 6]])
y = x[[0, 1, 2], [0, 1, 0]]
print(y)

# 以下实例获取了 4X3 数组中的四个角的元素。 行索引是 [0,0] 和 [3,3]，而列索引是 [0,2] 和 [0,2]。
x = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
print('我们的数组是：')
print(x)
print('\n')
rows = np.array([[0, 0], [3, 3]])
cols = np.array([[0, 2], [0, 2]])
y = x[rows, cols]
print('这个数组的四个角元素是：')
print(y)  # 返回的结果是包含每个角元素的 ndarray 对象。

# 可以借助切片 : 或 … 与索引数组组合
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = a[1:3, 1:3]
c = a[1:3, [1, 2]]
d = a[..., 1:]
print("a:", a)
print("b:", b)
print("c:", c)
print("d:", d)

# 布尔索引
# 我们可以通过一个布尔数组来索引目标数组。
# 布尔索引通过布尔运算（如：比较运算符）来获取符合指定条件的元素的数组。
# 以下实例获取大于 5 的元素：
x = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
print('我们的数组是：')
print(x)
print('\n')
# 现在我们会打印出大于 5 的元素
print('大于 5 的元素是：')
print(x[x > 5])

# 以下实例使用了 ~（取补运算符）来过滤 NaN。
a = np.array([np.nan, 1, 2, np.nan, 3, 4, 5])
print(a)
print(a[~np.isnan(a)])

# 以下实例演示如何从数组中过滤掉非复数元素。
a = np.array([1, 2 + 6j, 5, 3.5 + 5j])
print(a[np.iscomplex(a)])

# 花式索引
# 花式索引指的是利用整数数组进行索引。
# 花式索引根据索引数组的值作为目标数组的某个轴的下标来取值。
# 对于使用一维整型数组作为索引，如果目标是一维数组，那么索引的结果就是对应位置的元素，如果目标是二维数组，那么就是对应下标的行。
# 花式索引跟切片不一样，它总是将数据复制到新数组中。
#
# 一维数组
# 一维数组只有一个轴 axis = 0，所以一维数组就在 axis = 0 这个轴上取值：
x = np.arange(9)
print(x)
# 一维数组读取指定下标对应的元素
print("-------读取下标对应的元素-------")
x2 = x[[0, 6]]  # 使用花式索引
print(x2)

print(x2[0])
print(x2[1])

# 二维数组
# 1、传入顺序索引数组
x = np.arange(32).reshape((8, 4))
print(x)
# 二维数组读取指定下标对应的行
print("-------读取下标对应的行-------")
# 输出下标为 4, 2, 1, 7 对应的行
print(x[[4, 2, 1, 7]])

# 2、传入倒序索引数组
x = np.arange(32).reshape((8, 4))
print(x[[-4, -2, -1, -7]])

# 3、传入多个索引数组（要使用 np.ix_）
# np.ix_ 函数就是输入两个数组，产生笛卡尔积的映射关系。
# 笛卡尔乘积是指在数学中，两个集合 X 和 Y 的笛卡尔积（Cartesian product），又称直积，表示为 X×Y，第一个对象是X的成员而第二个对象是 Y 的所有可能有序对的其中一个成员。
#
# 例如 A={a,b}, B={0,1,2}，则：
# A×B={(a, 0), (a, 1), (a, 2), (b, 0), (b, 1), (b, 2)}
# B×A={(0, a), (0, b), (1, a), (1, b), (2, a), (2, b)}
x = np.arange(32).reshape((8, 4))
print("x: ", x)
print(x[np.ix_([1, 5, 7, 2], [0, 3, 1, 2])])

# NumPy 广播(Broadcast)
# 广播(Broadcast)是 numpy 对不同形状(shape)的数组进行数值计算的方式， 对数组的算术运算通常在相应的元素上进行。
# 如果两个数组 a 和 b 形状相同，即满足 a.shape == b.shape，那么 a*b 的结果就是 a 与 b 数组对应位相乘。这要求维数相同，且各维度的长度相同。
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])
c = a * b
print(c)

# 当运算中的 2 个数组的形状不同时，numpy 将自动触发广播机制
a = np.array([[0, 0, 0],
              [10, 10, 10],
              [20, 20, 20],
              [30, 30, 30]])
b = np.array([0, 1, 2])
print(a + b)

# 4x3 的二维数组与长为 3 的一维数组相加，等效于把数组 b 在二维上重复 4 次再运算：
a = np.array([[0, 0, 0],
              [10, 10, 10],
              [20, 20, 20],
              [30, 30, 30]])
b = np.array([1, 2, 3])
bb = np.tile(b, (4, 1))  # 重复 b 的各个维度
print(a + bb)
