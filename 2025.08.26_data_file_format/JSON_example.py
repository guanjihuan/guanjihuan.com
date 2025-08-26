import json

data = {
    "name": "Guan",
    "year": 1993,
    "hobbies": ["coding", "reading"],
}

# 写入
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4) # indent 使输出格式化，更易读

# 读取
with open('data.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)
    print(loaded_data)
    print(loaded_data['name'])