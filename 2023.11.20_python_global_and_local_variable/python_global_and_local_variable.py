"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/37736
"""

def my_function():
    x = 10  # 局域变量
    print('\n函数中的局域变量 x：', x)

my_function()
# print(x)  # 这里会引发错误，因为 x 在函数外不可访问
print()


y0 = 20  # 全局变量
y1 = 21  # 全局变量
def another_function():
    print('在函数中访问全局变量 y0：', y0) # 这里可以访问全局变量
    # print(y1) # 这里会引发错误，因为下面定义了局域变量，所以这里没法访问外面的全局变量
    y1 = 25  # 局域变量
    print('函数中的局域变量 y1：', y1)

another_function()
print('函数内部修改的局部变量不影响外部的全局变量 y1：', y1)  # 函数内部修改的局部变量不影响外部的全局变量
print()


z = 30  # 全局变量
def another_function_2():
    global z   # 使用 global 关键字来声明，从而可以在函数内修改全局变量
    print('通过global声明后，在函数中访问全局变量 z：', z)  
    z = 35
    print('在函数中修改全局变量 z：', z)

another_function_2()
print('被修改后的全局变量 z：', z, '\n')  # global 关键字声明后，函数内部修改的全局变量在函数外部也生效