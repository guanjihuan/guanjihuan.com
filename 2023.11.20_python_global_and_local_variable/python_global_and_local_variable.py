"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/37736
"""

def my_function():
    x = 10  # 局部变量
    print(x)

my_function()
# print(x)  # 这里会引发错误，因为 x 在函数外不可访问
print()


y = 20  # 全局变量
def another_function():
    y = 25  # 局域变量
    print(y)

another_function()
print(y)  # 函数内部修改的局部变量不影响外部的全局变量
print()


z = 20  # 全局变量
def another_function_2():
    global z   # 使用 global 关键字来声明，从而可以在函数内修改全局变量
    z = 25
    print(z)

another_function_2()
print(z)  # global 关键字声明后，函数内部修改的全局变量在函数外部也生效