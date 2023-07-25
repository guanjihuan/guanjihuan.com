"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/14684
"""

import sympy


# 定义符号
print()
print('定义符号：')
x, y, z = sympy.symbols('x y z')  # 使用sympy.symbols
print(x)
print(y+1)
print(z**2)
print()


# 替换（Substitution）
print('变量替换：')
expression_1 = x**2+1
value_1 = expression_1.subs(x, 3)  # 使用.subs()方法
print(value_1)
print()


# 字符串转成符号表达式
print('字符串转成符号表达式：')
expression_string = 'x**3+1'
print(expression_string)
expression_2 = sympy.sympify(expression_string)  # 使用sympy.sympify()
print(expression_2)
value_2 = expression_2.subs(x, 2)
print(value_2)
print()


# 简化表达式
print('简化表达式：')
expression_3 = sympy.simplify(sympy.sin(x)**2 + sympy.cos(x)**2)  # 使用sympy.simplify()
print(expression_3)
print()


# 符号矩阵
print('符号矩阵：')
a, b = sympy.symbols('a b')
matrix = sympy.Matrix([[1, a], [0, b]])   # 使用sympy.Matrix()
print(matrix)
print()


sympy.init_printing(use_unicode=True)
# 符号矩阵的特征值和特征向量
print('符号矩阵的特征值和特征向量：')
eigenvalue = matrix.eigenvals()  # 使用.eigenvals()方法
print('特征值\n', eigenvalue, '\n')
sympy.pprint(eigenvalue)               # 使用sympy.pprint()输出
print('\n', sympy.pretty(eigenvalue))  # 使用sympy.pretty()美化后输出
print()

eigenvector = matrix.eigenvects() # 使用.eigenvects()方法
print('特征向量\n', eigenvector, '\n')
sympy.pprint(eigenvector)
print('\n', sympy.pretty(eigenvector)) 
print()

P, D = matrix.diagonalize()  # 使用.diagonalize()方法
print('特征值\n', D, '\n')
print(sympy.pretty(D), '\n')
print('特征向量\n', P, '\n')
print(sympy.pretty(P), '\n')
print()

print('特征值\n', D.subs(a, -4).subs(b, 2), '\n')
print(sympy.pretty(D.subs(a, -4).subs(b, 2)), '\n')
print('特征向量\n', P.subs(a, -4).subs(b, 2), '\n')
print(sympy.pretty(P.subs(a, -4).subs(b, 2)), '\n')
print()

# 和numpy对比
print('和numpy对比：')
import numpy as np
matrix = np.array([[1, -4], [0, 2]])
eigenvalue, eigenvector = np.linalg.eig(matrix) 
print('特征值\n', eigenvalue)
print('特征向量\n', eigenvector)
print()