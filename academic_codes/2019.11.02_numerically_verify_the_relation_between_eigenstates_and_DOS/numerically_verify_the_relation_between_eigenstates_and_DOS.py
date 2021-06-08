"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/962
"""

import numpy as np


def hamiltonian(width=2, length=4):  # 有一定宽度和长度的方格子
    h00 = np.zeros((width*length, width*length))
    for i0 in range(length):
        for j0 in range(width-1):
            h00[i0*width+j0, i0*width+j0+1] = 1
            h00[i0*width+j0+1, i0*width+j0] = 1
    for i0 in range(length-1):
        for j0 in range(width):
            h00[i0*width+j0, (i0+1)*width+j0] = 1
            h00[(i0+1)*width+j0, i0*width+j0] = 1
    return h00


def main():
    h0 = hamiltonian()
    dim = h0.shape[0]
    n = 4  # 选取第n个能级
    eigenvalue, eigenvector = np.linalg.eig(h0)  # 本征值、本征矢
    # print(h0)
    # print('哈密顿量的维度：', dim)  # 哈密顿量的维度
    # print('本征矢的维度：', eigenvector.shape)  # 本征矢的维度
    # print('能级（未排序）：', eigenvalue)  # 输出本征值。因为体系是受限的，所以是离散的能级
    # print('选取第', n, '个能级，为',  eigenvalue[n-1])  # 从1开始算，查看第n个能级是什么（这里本征值未排序）
    # print('第', n, '个能级对应的波函数：', eigenvector[:, n-1])  # 查看第n个能级对应的波函数
    print('\n波函数模的平方：\n', np.square(np.abs(eigenvector[:, n-1])))   # 查看第n个能级对应的波函数模的平方
    green = np.linalg.inv((eigenvalue[n-1]+1e-15j)*np.eye(dim)-h0)  # 第n个能级对应的格林函数
    total = np.trace(np.imag(green))  # 求该能级格林函数的迹，对应的是总态密度（忽略符号和系数）
    print('归一化后的态密度分布：')
    for i in range(dim):
        print(np.imag(green)[i, i]/total)  # 第n个能级单位化后的态密度分布
    print('观察以上两个分布的数值情况，可以发现两者完全相同。')


if __name__ == '__main__':
    main()
