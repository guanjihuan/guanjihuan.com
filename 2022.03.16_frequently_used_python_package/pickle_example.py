import pickle

data = [1, 2, 3]

# 保存为文件
with open('a.pkl', 'wb') as f:
    pickle.dump(data, f)
with open('a.pkl', 'rb') as f:
    data_load_from_file = pickle.load(f)
print(data_load_from_file)
print()

# 把对象转换成字节流
serialized_data = pickle.dumps(data) # 转换成字节流
print(type(serialized_data))
print(serialized_data)
print()
loaded_data = pickle.loads(serialized_data) # 转换成原类型
print(type(loaded_data))
print(loaded_data)