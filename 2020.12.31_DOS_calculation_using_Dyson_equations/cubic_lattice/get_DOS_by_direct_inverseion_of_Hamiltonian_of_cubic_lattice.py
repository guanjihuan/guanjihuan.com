"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/7650
"""

import numpy as np

def hamiltonian(width, length, height):  
    h = np.zeros((width*length*height, width*length*height))
    for i0 in range(length):
        for j0 in range(width):
            for k0 in range(height-1):
                h[k0*width*length+i0*width+j0, (k0+1)*width*length+i0*width+j0] = 1
                h[(k0+1)*width*length+i0*width+j0, k0*width*length+i0*width+j0] = 1
    for i0 in range(length):
        for j0 in range(width-1):
            for k0 in range(height):
                h[k0*width*length+i0*width+j0, k0*width*length+i0*width+j0+1] = 1
                h[k0*width*length+i0*width+j0+1, k0*width*length+i0*width+j0] = 1
    for i0 in range(length-1):
        for j0 in range(width):
            for k0 in range(height):
                h[k0*width*length+i0*width+j0, k0*width*length+(i0+1)*width+j0] = 1
                h[k0*width*length+(i0+1)*width+j0, k0*width*length+i0*width+j0] = 1
    return h

def main():
    height = 2  # z
    width = 3  # y
    length = 4  # x
    h = hamiltonian(width, length, height)
    E = 0
    green = np.linalg.inv((E+1e-2j)*np.eye(width*length*height)-h)  
    for k0 in range(height):
        print('z=', k0+1, ':')
        for j0 in range(width):
            print('      y=', j0+1, ':')
            for i0 in range(length):
                print('             x=', i0+1, ' ', -np.imag(green[k0*width*length+i0*width+j0, k0*width*length+i0*width+j0])/np.pi)   # 态密度

if __name__ == "__main__":
    main()