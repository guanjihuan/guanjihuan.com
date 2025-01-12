a = [1, 2] # list列表
print(a)
print(type(a)) # 对象类型
print(id(a))  # 对象唯一标识符
print(len(a)) # 列表长度
a.append(3) # list列表增加元素
print(a)
print(sum(a))  # 求和
print(max(a)) # 最大值
print(min(a)) # 最小值
print(abs(-3.14)) # 绝对值
b1 = [2, -1, 3]
b2 = sorted(b1) # 排序，不改变原数列
print(b1)
print(b2)
b3 = list(reversed(b1)) # 反向并转为list列表
print(b1)
print(b3)
c = range(5)  # 数列，从0开始
print(c)
for i0 in c:
    print(i0)
d1 = [1, 2, 3, 3, 2, 1, 1]
d2 = set(d1) # 转成集合，去除重复元素
print(d1)
print(d2)
print(list(d2))

print()
dict_data = {"name": "张三", "age": 30, "city": "北京"} # dict字典
print(dict_data)
print(type(dict_data))
print(dict_data.items())
for key, value in dict_data.items():
    print(f'打印字典内容 {key} {value}')

print() # 打印空一行
print(all([True, True, False])) # 所有元素为真，结果为真
print(all([1, 2, True]))
print(any([True, True, False])) # 有一个是真，结果为真
print(any([0, None, ""]))

print()
e = 'abc'
print(e)
print(hash(e)) # 哈希值（如果是多次运行，对于相同的对象，返回的哈希值是不同的）
print(hash(e)) # 哈希值（同一个运行中多次调用 hash()，对于相同的对象，返回的哈希值是相同的）

print()
for i0 in range(3):
    exec(f'''
a{i0} = {i0}
print(a{i0})
''')  # 执行动态创建的代码
f = eval('1+2') # 执行表达式并返回值
print(f)

f = open('a.txt', 'w') # 打开文件
f.write('test') # 写入文件
f.close() # 关闭文件