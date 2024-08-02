import json
import pandas as pd
from glom import glom

print(pd.__version__)

"""
mydataset = {
    'sites': ["Google", "Runoob", "Wiki"],
    'number': [1, 2, 3]
}

myvar = pd.DataFrame(mydataset)
print(myvar)

a = [1, 2, 3]
myseries = pd.Series(a)
print(myseries)
print(myseries[1])

a = ["Google", "Runoob", "Wiki"]
myseries = pd.Series(a, index=["x", "y", "z"])
print(myseries)
print(myseries['y'])



# 使用列表创建
data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
df = pd.DataFrame(data, columns=['Site', 'Age'])
print(df)
# print(df['Site'])

# 使用 ndarrays 创建
data = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
df = pd.DataFrame(data)
print(df)
# print(df['Age'])


# 使用字典（key/value），其中字典的 key 为列名:
data = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
df = pd.DataFrame(data)
print(df)


data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}
# 数据载入到 DataFrame 对象
df = pd.DataFrame(data)
print(df)
# 返回第一行, 返回结果其实就是一个 Pandas Series 数据。
print(df.loc[0])
# 返回第二行
print(df.loc[1])
# 返回第一行和第二行, 返回结果其实就是一个 Pandas DataFrame 数据。
print(df.loc[[0, 1]])


data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}
df = pd.DataFrame(data, index = ["day1", "day2", "day3"])
print(df)
# 指定索引
print(df.loc["day2"])

"""

"""
df = pd.read_csv('./nba.csv')
print(df)
# to_string() 用于返回 DataFrame 类型的数据，如果不使用该函数，则输出结果为数据的前面 5 行和末尾 5 行，中间部分以 ... 代替。
print(df.to_string())
# head( n ) 方法用于读取前面的 n 行，如果不填参数 n ，默认返回 5 行。
print(df.head())
print(df.head(10))
# tail( n ) 方法用于读取尾部的 n 行，如果不填参数 n ，默认返回 5 行，空行各个字段的值返回 NaN。
print(df.tail())
print(df.tail(10))
# info() 方法返回表格的一些基本信息：
print(df.info())
"""

"""
# 三个字段 name, site, age
nme = ["Google", "Runoob", "Taobao", "Wiki"]
st = ["www.google.com", "www.runoob.com", "www.taobao.com", "www.wikipedia.org"]
ag = [90, 40, 80, 98]
# 字典
dict = {'name': nme, 'site': st, 'age': ag}
df = pd.DataFrame(dict)
print(df)
# 保存 dataframe
df.to_csv('./site.csv')
"""

"""
df = pd.read_csv('./nba.csv')
print(df)
# to_string() 用于返回 DataFrame 类型的数据，如果不使用该函数，则输出结果为数据的前面 5 行和末尾 5 行，中间部分以 ... 代替。
print(df.to_string())
# head( n ) 方法用于读取前面的 n 行，如果不填参数 n ，默认返回 5 行。
print(df.head())
print(df.head(10))
# tail( n ) 方法用于读取尾部的 n 行，如果不填参数 n ，默认返回 5 行，空行各个字段的值返回 NaN。
print(df.tail())
print(df.tail(10))
# info() 方法返回表格的一些基本信息：
print(df.info())
"""

"""
# 
df = pd.read_json('./sites.json')
# to_string() 用于返回 DataFrame 类型的数据
print(df.to_string())

# 直接处理 JSON 字符串。
data = [
    {
        "id": "A001",
        "name": "菜鸟教程",
        "url": "www.runoob.com",
        "likes": 61
    },
    {
        "id": "A002",
        "name": "Google",
        "url": "www.google.com",
        "likes": 124
    },
    {
        "id": "A003",
        "name": "淘宝",
        "url": "www.taobao.com",
        "likes": 45
    }
]
df = pd.DataFrame(data)
print(df)

# JSON 对象与 Python 字典具有相同的格式，所以我们可以直接将 Python 字典转化为 DataFrame 数据：
# 字典格式的 JSON
s = {
    "col1": {"row1": 1, "row2": 2, "row3": 3},
    "col2": {"row1": "x", "row2": "y", "row3": "z"}
}

# 读取 JSON 转为 DataFrame
df = pd.DataFrame(s)
print(df)

# 从 URL 中读取 JSON 数据：
URL = 'https://static.runoob.com/download/sites.json'
df = pd.read_json(URL)
print(df)

# 内嵌的 JSON 数据文件
df = pd.read_json('nested_list.json')
# print(df)
# 需要使用到 json_normalize() 方法将内嵌的数据完整的解析出来：
# 使用 Python JSON 模块载入数据
with open('./nested_list.json', 'r') as f:
    data = json.loads(f.read())
# 展平数据
df_nested_list = pd.json_normalize(data, record_path=['students'])
print(df_nested_list)
# data = json.loads(f.read()) 使用 Python JSON 模块载入数据。
# json_normalize() 使用了参数 record_path 并设置为 ['students'] 用于展开内嵌的 JSON 数据 students。
# 显示结果还没有包含 school_name 和 class 元素，如果需要展示出来可以使用 meta 参数来显示这些元数据：


# 使用 Python JSON 模块载入数据
with open('nested_list.json', 'r') as f:
    data = json.loads(f.read())
# 展平数据
df_nested_list = pd.json_normalize(
    data,
    record_path=['students'],
    meta=['school_name', 'class']
)
print(df_nested_list)
"""

"""
# 使用 Python JSON 模块载入数据
with open('nested_mix.json', 'r') as f:
    data = json.loads(f.read())

df = pd.json_normalize(
    data,
    record_path=['students'],
    meta=[
        'class',
        ['info', 'president'],
        ['info', 'contacts', 'tel'],
        ['info', 'contacts', 'email'],
        'school_name'
    ]
)
print(df)

# 读取内嵌数据中的一组数据
# 这里我们需要使用到 glom 模块来处理数据套嵌，glom 模块允许我们使用 . 来访问内嵌对象的属性。
df = pd.read_json('./nested_deep.json')
# data = df['students'].apply(lambda row: glom(row, 'grade.*'))
data = df['students'].apply(lambda row: glom(row, 'grade.math'))
print(data)

"""

"""

# Pandas 数据清洗
df = pd.read_csv('./property-data.csv')
print(df['NUM_BEDROOMS'])
print(df['NUM_BEDROOMS'].isnull())

# Pandas 把 n/a 和 NA 当作空数据，na 不是空数据，不符合我们要求，我们可以指定空数据类型：
# 指定空数据类型：
missing_values = ["n/a", "na", "--"]
df = pd.read_csv('./property-data.csv', na_values=missing_values)
print(df['NUM_BEDROOMS'])
print(df['NUM_BEDROOMS'].isnull())

# 默认情况下，dropna() 方法返回一个新的 DataFrame，不会修改源数据。
# 如果你要修改源数据 DataFrame, 可以使用 inplace = True 参数:
# df.dropna(inplace=True)
df_new = df.dropna()  # 删除包含空数据的行。
print(df_new.to_string())

"""

"""

# 移除指定列有空值的行：
# 移除 ST_NUM 列中字段值为空的行：
df = pd.read_csv('./property-data.csv')
print(df.to_string())
# df.dropna(subset=['ST_NUM'], inplace=True)
df_new = df.dropna(subset=['ST_NUM'])
print(df_new.to_string())

# fillna()方法来替换一些空字段：
df = pd.read_csv('./property-data.csv')
print(df.to_string())
# df.fillna(12345, inplace=True)
df_new = df.fillna(12345)
print(df_new.to_string())

# 我们也可以指定某一个列来替换数据：
df = pd.read_csv('./property-data.csv')
# df['PID'].fillna(12345, inplace=True)
df_new = df['PID'].fillna(12345)
print(df_new.to_string())

# 替换空单元格的常用方法是计算列的均值、中位数值或众数。
# Pandas使用 mean()、median() 和 mode() 方法计算列的均值（所有值加起来的平均值）、中位数值（排序后排在中间的数）和众数（出现频率最高的数）。
df = pd.read_csv('property-data.csv')
x = df["ST_NUM"].mean()      # 使用 mean() 方法计算列的均值并替换空单元格：
# x = df["ST_NUM"].median()  # 使用 median() 方法计算列的中位数并替换空单元格：
# x = df["ST_NUM"].mode()    # 使用 mode() 方法计算列的众数并替换空单元格：


# df["ST_NUM"].fillna(x, inplace=True)
df_new = df["ST_NUM"].fillna(x)
print(df_new.to_string())
"""

"""

# Pandas 清洗格式错误数据
# 数据格式错误的单元格会使数据分析变得困难，甚至不可能。
# 我们可以通过包含空单元格的行，或者将列中的所有单元格转换为相同格式的数据。
# 以下实例会格式化日期：
# 第三个日期格式错误
data = {
    "Date": ['2020/12/01', '2020/12/02', '20201226', '2021-12-26'],
    "duration": [50, 40, 45, 50]
}
df = pd.DataFrame(data, index=["day1", "day2", "day3", "day4"])
df['Date'] = pd.to_datetime(df['Date'], format='mixed')
print(df.to_string())

# Pandas 清洗错误数据
# 数据错误也是很常见的情况，我们可以对错误的数据进行替换或移除。
# 以下实例会替换错误年龄的数据：
person = {
    "name": ['Google', 'Runoob', 'Taobao'],
    "age": [50, 40, 12345]  # 12345年龄数据是错误的
}
df = pd.DataFrame(person)
print(df.to_string())
print(df.loc[2])
print(df.loc[2, 'age'])
print(df.loc[2, 'name'])
df.loc[2, 'age'] = 30  # 修改数据
print(df.to_string())

# 也可以设置条件语句：
# 将 age 大于 120 的设置为 120:
person = {
    "name": ['Google', 'Runoob', 'Taobao'],
    "age": [50, 200, 12345]
}
df = pd.DataFrame(person)
for x in df.index:
    if df.loc[x, "age"] > 120:
        df.loc[x, "age"] = 120
print(df.to_string())

# 也可以将错误数据的行删除：
person = {
    "name": ['Google', 'Runoob', 'Taobao'],
    "age": [50, 40, 12345]  # 12345 年龄数据是错误的
}
df = pd.DataFrame(person)
for x in df.index:
    if df.loc[x, "age"] > 120:
        df.drop(x, inplace=True)
print(df.to_string())

#
# Pandas 清洗重复数据
# 如果我们要清洗重复数据，可以使用 duplicated() 和 drop_duplicates() 方法。
# 如果对应的数据是重复的，duplicated() 会返回 True，否则返回 False。
person = {
    "name": ['Google', 'Runoob', 'Runoob', 'Taobao'],
    "age": [50, 40, 40, 23]
}
df = pd.DataFrame(person)
print(df.duplicated())
# 删除重复数据，可以直接使用drop_duplicates() 方法。
# By default, it removes duplicate rows based on all columns.
df.drop_duplicates(inplace=True)
print(df)

df = pd.DataFrame(person)
# To remove duplicates on specific column(s), use subset.
df_new = df.drop_duplicates(subset=['name'])
print(df_new)

df = pd.DataFrame(person)
# # To remove duplicates and keep last occurrences, use keep.
df_new = df.drop_duplicates(subset=['name'], keep='last')
df_new = df.drop_duplicates(subset=['name', 'age'], keep='last')
print(df_new)
# 选择指定的列
print(df_new.filter(items=['name']))
# 选择列名匹配正则表达式的列
print(df_new.filter(regex='age'))
# 随机选择 n 行数据
print(df_new.sample(n=2))

# 按照指定列的值排序
df_new.sort_values('name')
# 按照多个列的值排序
df_new.sort_values(['name', 'age'], ascending=True)
# 按照索引排序
df_new.sort_index()
print(df_new)

"""

# 读取 JSON 数据
df = pd.read_json('data.json')
print(df)
# 删除缺失值
# df = df.dropna()
# print(df)
# 用指定的值填充缺失值
df = df.fillna({'age': 0, 'score': 0})
print(df)

# # 重命名列名
df = df.rename(columns={'name': '姓名', 'age': '年龄', 'gender': '性别', 'score': '成绩'})
print(df)
# # 按成绩排序
df = df.sort_values(by='成绩', ascending=False)
print(df)
# # 按性别分组并计算平均年龄和成绩
grouped = df.groupby('性别').agg({'年龄': 'mean', '成绩': 'mean'})
print(grouped)
# # 选择成绩大于等于90的行，并只保留姓名和成绩两列
df = df.loc[df['成绩'] >= 90, ['姓名', '成绩', '年龄']]
print(df)
# # 计算每列的基本统计信息
stats = df.describe()
print(stats)

df = pd.read_json('data.json')
# # 计算每列的平均值
mean = df['score'].mean()
print("平均成绩为： ", mean)
# # 计算每列的中位数
median = df['score'].median()
print("中位数为：", median)
# # 计算每列的众数
mode = df['score'].mode()
print("众数为：", mode)
# # 计算每列非缺失值的数量
count = df.count()
print(type(count))