"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/417
"""

import numpy as np

# Python基本操作【循环，判断，函数，文件写入】
for i in range(5):  # 循环（这里只举例for循环，要了解while循环可自行搜索资料）
    print('我是循环产生的数：', i)  # Python中没有end，所以缩进很重要，不能省！
    if i == 2:   # 判断
        print('判断：我是第三个数 2')
    else:
        pass  # pass代表不执行任何语句，用于占位，可以之后再补充，不然空着会报错
print()  # 空一行


def fun0(arg):  # 定义函数
    print('我是函数中的内容，参数值为：', arg)  # \n代表换行
    return arg*2  # 返回值


print('函数返回值：', fun0(5), '\n')  # 调用函数
# 关于类class，这里不举例了。科学计算中主要还是面向过程，面向对象用的比较少。有需要了解的可以自行搜索资料。

# 文件写入
# 第一种方式
with open('test1.txt', 'w') as f1:   # 其中'w'为重新写入，改为'a'是补充内容
    f1.write(str(100)+'\n这是第一种方式写入文件')  # str()为转换成字符串
# 第二种方式
f2 = open('test2.txt', 'w')  # 打开文件
f2.write(str(200)+'\n这是第二种方式写入文件')  # 写入文件
f2.close()  # 关闭文件


# Numpy库中常用的语句
print('零矩阵：\n', np.zeros((2, 3)))  # 注意np.zeros()里需要填元组，因此是两个括号
print('单位矩阵：\n', np.identity(3))    # 3行3列的单位矩阵,或者可以用np.eye()
print('把一维数组按对角矩阵排列：\n', np.diag([1, 3, 5]), '\n')

print('指定步长的等差数列：\n', np.arange(1, 5, .5))  # 区间是左闭右开[1, 5)
print('指定个数的等差数列：\n', np.linspace(-2, 2, 5), '\n')  # 区间是左闭右闭[-2, 2], 数量是5

print('随机数：\n', np.random.uniform(-2, 2))  # 区间是左闭右开[-2, 2)
print('随机整数：\n', np.random.randint(-10, 10), '\n')  # 区间是左闭右闭[-10, 10]

print('数组从小到大排列：\n', np.sort([1, 7, 0, 3]))
print('数组从小到大排列对应的索引：\n', np.argsort([1, 7, 0, 3]), '\n')  # 注意Python中下标是从0开始的

matrix0 = np.array([[1, 2+9j, 3], [2, 5, 7]])
print('矩阵0：\n', matrix0)
print('矩阵的维度：\n', matrix0.shape)  # 查看矩阵的维度
print('矩阵的行数：\n', matrix0.shape[0])  # 查看矩阵的行数
print('矩阵的列数：\n', matrix0.shape[1])  # 查看矩阵的列数
print('矩阵转置：\n', matrix0.transpose())  # 矩阵转置
print('矩阵转置共轭：\n', matrix0.transpose().conj(), '\n')  # 矩阵转置共轭

matrix1 = np.array([[3, 5], [2, 7]])  # numpy数组
eigenvalue, eigenvector = np.linalg.eig(matrix1)  # 求本征值，本征向量
print('矩阵1：\n', matrix1)
print('本征值：\n', eigenvalue)
print('本征向量：\n', eigenvector) # 列向量对应的是本征矢量
print('逆矩阵：\n', np.linalg.inv(matrix1))
print('计算行列式：\n', np.linalg.det(matrix1), '\n')

matrix2 = np.array([[1, 2], [3, 4]])
print('矩阵2：\n', matrix2)
print('矩阵1和矩阵2相乘：\n', np.matmul(matrix1, matrix2), '\n')  # 矩阵乘积，或者可以用np.dot()

a = np.array([1, 2])
print('数组a=', a)
b = np.array([3, 4])
print('数组b=', b)
print('增加元素：\n', np.append(a, b, axis=0))  # 增加元素
print('增加行：\n', np.append([a], [b], axis=0))  # 增加行（列数要相同），或者用np.row_stack(([a], [b]))
print('增加列：\n', np.append([a], [b], axis=1))  # 增加列（行数要相同），或者用np.column_stack(([a], [b]))
