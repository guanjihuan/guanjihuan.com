# 小数的格式化输出（浮点）
value = 3.141592653589793
print(f"pi={value:.2f}")
print("pi={:.2f}".format(value))
print("pi=%.2f" % value)

# 整数的格式化输出
value = 13
print(f"a={value:5d}")
print("a={:5d}".format(value))
print("a=%5d" % value)