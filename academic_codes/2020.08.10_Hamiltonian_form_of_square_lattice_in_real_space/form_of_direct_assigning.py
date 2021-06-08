"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/5375
"""

import numpy as np

def hamiltonian(width=3, length=3):   # 方格子哈密顿量
    h = np.zeros((width*length, width*length))
    # y方向的跃迁
    for x in range(length):
        for y in range(width-1):
            h[x*width+y, x*width+y+1] = 1
            h[x*width+y+1, x*width+y] = 1
    # x方向的跃迁
    for x in range(length-1):
        for y in range(width):
            h[x*width+y, (x+1)*width+y] = 1
            h[(x+1)*width+y, x*width+y] = 1
    return h

h = hamiltonian()
print(h)