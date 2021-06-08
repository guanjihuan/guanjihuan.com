import numpy as np
from math import *  
# import os
# os.chdir('D:/data')  # 设置路径


def main():
    k1 = np.arange(-pi, pi, 0.05)
    k2 = np.arange(-pi, pi, 0.05)
    value = np.ones((k2.shape[0], k1.shape[0]))
    write_matrix(k1, k2, value)


def write_matrix(k1, k2, matrix):
    with open('a.txt', 'w') as f:
        # np.set_printoptions(suppress=True)  # 取消输出科学记数法
        f.write('0           ')
        for k10 in k1:
            f.write(str(k10)+'   ')
        f.write('\n')
        i0 = 0
        for k20 in k2:
            f.write(str(k20))
            for j0 in range(k1.shape[0]):
                f.write('  '+str(matrix[i0, j0])+'   ')
            f.write('\n')
            i0 += 1   


if __name__ == '__main__':
    main()