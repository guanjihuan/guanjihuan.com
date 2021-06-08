"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/5375
"""

import numpy as np

def hamiltonian(width=3, length=3):   # 方格子哈密顿量
    hopping_x = np.zeros((length, length))
    hopping_y = np.zeros((width, width))
    for i in range(length-1):
        hopping_x[i, i+1] = 1
        hopping_x[i+1, i] = 1
    for i in range(width-1):
        hopping_y[i, i+1] = 1
        hopping_y[i+1, i] = 1
    h = np.kron(hopping_x, np.eye(width))+np.kron(np.eye(length), hopping_y)
    return h

h = hamiltonian()
print(h)