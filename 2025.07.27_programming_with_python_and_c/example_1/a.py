from ctypes import cdll

lib = cdll.LoadLibrary("libc.so.6")  # Linux 系统
# lib = cdll.msvcrt  # Windows 系统

# 调用 C 标准库中的 printf 函数，字符串需要编码为 bytes
message = b"Hello, ctypes!\n"
result = lib.printf(message)
print(result)