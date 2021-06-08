"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/7650
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *


def hamiltonian(width, length):  
    h = np.zeros((width*length, width*length))
    for i0 in range(length):
        for j0 in range(width-1):
            h[i0*width+j0, i0*width+j0+1] = 1
            h[i0*width+j0+1, i0*width+j0] = 1
    for i0 in range(length-1):
        for j0 in range(width):
            h[i0*width+j0, (i0+1)*width+j0] = 1
            h[(i0+1)*width+j0, i0*width+j0] = 1
    return h


def main():
    width = 2
    length = 3
    h = hamiltonian(width, length)
    E = 0
    green = np.linalg.inv((E+1e-2j)*np.eye(width*length)-h)  
    for i0 in range(length):
        # print('G_{'+str(i0+1)+','+str(i0+1)+'}^{('+str(length)+')}:')
        # print(green[i0*width+0: i0*width+width, i0*width+0: i0*width+width], '\n') 
        print('x=', i0+1, ':')
        for j0 in range(width):
            print('     y=', j0+1, ' ', -np.imag(green[i0*width+j0, i0*width+j0])/pi) 


if __name__ == "__main__":
    main()

   