import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root123', database='test_db', charset='utf8')
cur = conn.cursor()

command = "insert into user values(0,'wang wu', 24), (0, 'chen liu', 27);"
rows_affected = cur.execute(command)
print(rows_affected)

command = "select * from user;"
cur.execute(command)

for line in cur.fetchall():
    print(line)

# 只要是对数据库中的数据进行修改 就需要进行提交操作 否则不会真正的修改
conn.commit()

cur.close()
conn.close()
