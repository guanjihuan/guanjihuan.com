import numpy as np
from math import *  
# import os
# os.chdir('D:/data')  # 设置路径


def main():
    k1 = np.arange(-pi, pi, 0.05)
    k2 = np.arange(-pi, pi, 0.05)
    value = np.ones((k2.shape[0], k1.shape[0]))
    plot_matrix(k1, k2, value)


def plot_matrix(k1, k2, matrix):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    k1, k2 = np.meshgrid(k1, k2)
    ax.plot_surface(k1, k2, matrix, cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    plt.xlabel('k1')
    plt.ylabel('k2') 
    ax.set_zlabel('Z')  
    plt.show()


if __name__ == '__main__':
    main()