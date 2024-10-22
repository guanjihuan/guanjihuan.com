value = 3.141592653589793

# 非格式化输出
print("pi=", value) # 直接输出
print("pi="+str(value)) # 转成字符串输出
print(f"pi={value}") # 使用 f 形式

# 格式化输出 
print(f"pi={value:.2f}")
print("pi={:.2f}".format(value))
print("pi=%.2f" % value)