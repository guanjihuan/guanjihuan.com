"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/5025
"""


import numpy as np
import matplotlib.pyplot as plt
from math import * 
import cmath
import time

def hamiltonian(k):  # SSH模型
    v=0.6
    w=1
    matrix = np.zeros((2, 2), dtype=complex)
    matrix[0,1] = v+w*cmath.exp(-1j*k)
    matrix[1,0] = v+w*cmath.exp(1j*k)
    return matrix


def main():
    start_clock = time.perf_counter()
    delta_1 = 1e-9  # 求导的步长（求导的步长可以尽可能短）
    delta_2 = 1e-5  # 积分的步长（积分步长和计算时间相关，因此取一个合理值即可）
    W = 0  # Winding number初始化
    for k in np.arange(-pi, pi, delta_2):
        H = hamiltonian(k)
        log0 = cmath.log(H[0, 1])
    
        H_delta = hamiltonian(k+delta_1) 
        log1 = cmath.log(H_delta[0, 1])

        W = W + (log1-log0)/delta_1*delta_2 # Winding number
    print('Winding number = ', W/2/pi/1j)
    end_clock = time.perf_counter()
    print('CPU执行时间(min)=', (end_clock-start_clock)/60)


if __name__ == '__main__':
    main()
