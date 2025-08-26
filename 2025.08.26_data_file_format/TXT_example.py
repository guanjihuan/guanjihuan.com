# 写入
with open('data.txt', 'w', encoding='utf-8') as f:
    f.write('test_1\ntest_2')

# 读取
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read() # 读取全部内容
print(content)

with open('data.txt', 'r', encoding='utf-8') as f: 
    lines = f.readlines() # 或按行读取
print(lines)
for line in lines:
    print(line.strip()) # strip() 去除首尾空白字符