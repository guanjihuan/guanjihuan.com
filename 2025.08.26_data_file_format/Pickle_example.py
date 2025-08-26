import pickle

data = [1, 2, 3]

# 写入
with open('data.pkl', 'wb') as f: # 注意是 'wb' 二进制写入
    pickle.dump(data, f)

# 读取
with open('data.pkl', 'rb') as f: # 注意是 'rb' 二进制读取
    loaded_data = pickle.load(f)
    print(loaded_data)