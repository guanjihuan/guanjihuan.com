import sqlite3

# 1. 连接数据库（自动创建）
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# 2. 创建表
cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)')

# 3. 插入数据
cursor.execute("INSERT INTO users VALUES ('张三', 25)")
cursor.execute("INSERT INTO users VALUES ('李四', 30)")

# 4. 提交更改
conn.commit()

# 5. 读取数据
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

print("所有用户数据:")
for row in rows:
    print(f"姓名: {row[0]}, 年龄: {row[1]}")

# 6. 关闭连接
conn.close()