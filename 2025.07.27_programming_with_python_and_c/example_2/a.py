from ctypes import cdll

lib = cdll.LoadLibrary('./example.so')  # Linux 系统
# lib = cdll.LoadLibrary('./example.dll')  # Windows 系统

# 调用 C 函数
result = lib.add_two_numbers(3, 5)
print(result)