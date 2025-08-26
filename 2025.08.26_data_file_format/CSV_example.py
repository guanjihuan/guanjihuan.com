import csv

# 写入 CSV
with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'year', 'value']) # 写入表头
    writer.writerow(['Guan', 1993, 1])
    writer.writerow(['G123', 2025, 0])

# 读取 CSV
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row) # 每行是一个列表