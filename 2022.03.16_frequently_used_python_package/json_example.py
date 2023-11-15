import json

# 定义一个字典对象
data = {
    "name": "张三",
    "age": 30,
    "city": "北京"
}

print(type(data))
print(data.items())
for key, value in data.items():
    print(f'{key}: {value}')
print()

# 将字典对象转换为JSON格式
json_data = json.dumps(data)
print(type(json_data))
print("JSON格式数据：", json_data)
print()

# 将JSON格式数据转换回字典对象
dict_data = json.loads(json_data)
print(type(dict_data))
print("字典对象：", dict_data)