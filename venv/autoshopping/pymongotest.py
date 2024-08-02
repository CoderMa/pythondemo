from pymongo import MongoClient
# from pymongo import *

# 创建 MongoDB 客户端
client = MongoClient('mongodb://localhost:27017/')

# 获取数据库
db = client.test_database

# 获取集合
collection = db.test_collection

# 插入文档
result = collection.insert_one({"name": "Alice", "age": 30})

# 查找文档
document = collection.find_one({"name": "Alice"})
print(document)
