"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/8536
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *  
import cmath
import time


def hamiltonian(k1, k2, t1=2.82, a=1/sqrt(3)):  # 石墨烯哈密顿量（a为原子间距，不赋值的话默认为1/sqrt(3)）
    h = np.zeros((2, 2))*(1+0j)
    h[0, 0] = 0.28/2
    h[1, 1] = -0.28/2
    h[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h[0, 1] = h[1, 0].conj()
    return h


def main():
    start_time = time.time()
    n = 400  # 取点密度
    delta = 1e-10  # 求导的偏离量
    kx_array = np.linspace(-2*pi, 2*pi, n)
    ky_array = np.linspace(-2*pi, 2*pi, n)
    for band in range(2):
        F_all = np.zeros((ky_array.shape[0], ky_array.shape[0]))  # 贝里曲率
        j0 = 0
        for kx in kx_array:
            print(kx)
            i0 = 0
            for ky in ky_array:
                H = hamiltonian(kx, ky)
                eigenvalue, eigenvector = np.linalg.eig(H)
                vector = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]  # 价带波函数
                # print(np.argsort(np.real(eigenvalue))[0])  # 排序索引（从小到大）
                # print(eigenvalue)  # 排序前的本征值
                # print(np.sort(np.real(eigenvalue)))  # 排序后的本征值（从小到大）
            
                H_delta_kx = hamiltonian(kx+delta, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx)
                vector_delta_kx = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]   # 略偏离kx的波函数
                # vector_delta_kx = find_vector_with_the_same_gauge(vector_delta_kx, vector)  # 如果波函数不连续需要使用这个

                H_delta_ky = hamiltonian(kx, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_ky)
                vector_delta_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]  # 略偏离ky的波函数
                # vector_delta_ky = find_vector_with_the_same_gauge(vector_delta_ky, vector)  # 如果波函数不连续需要使用这个

                H_delta_kx_ky = hamiltonian(kx+delta, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx_ky)
                vector_delta_kx_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]  # 略偏离kx和ky的波函数
                # vector_delta_kx_ky = find_vector_with_the_same_gauge(vector_delta_kx_ky, vector)  # 如果波函数不连续需要使用这个

                # 价带的波函数的贝里联络(berry connection) # 求导后内积
                A_x = np.dot(vector.transpose().conj(), (vector_delta_kx-vector)/delta)   # 贝里联络Ax（x分量）
                A_y = np.dot(vector.transpose().conj(), (vector_delta_ky-vector)/delta)   # 贝里联络Ay（y分量）
                
                A_x_delta_ky = np.dot(vector_delta_ky.transpose().conj(), (vector_delta_kx_ky-vector_delta_ky)/delta)  # 略偏离ky的贝里联络Ax
                A_y_delta_kx = np.dot(vector_delta_kx.transpose().conj(), (vector_delta_kx_ky-vector_delta_kx)/delta)  # 略偏离kx的贝里联络Ay

                # 贝里曲率(berry curvature)
                F = ((A_y_delta_kx-A_y)/delta-(A_x_delta_ky-A_x)/delta)*1j
                # print(F)
                F_all[i0, j0] = np.real(F)
                i0 += 1
            j0 += 1

        if band==0:
            plot_3d_surface(kx_array/pi, ky_array/pi, F_all, xlabel='kx', ylabel='ky', zlabel='Berry curvature', title='Valence Band', rcount=300, ccount=300)
        else:
            plot_3d_surface(kx_array/pi, ky_array/pi, F_all, xlabel='kx', ylabel='ky', zlabel='Berry curvature', title='Conductance Band', rcount=300, ccount=300)
        # import guan
        # if band==0:
        #     guan.plot_3d_surface(kx_array/pi, ky_array/pi, F_all, xlabel='kx', ylabel='ky', zlabel='Berry curvature', title='Valence Band', rcount=300, ccount=300)
        # else:
        #     guan.plot_3d_surface(kx_array/pi, ky_array/pi, F_all, xlabel='kx', ylabel='ky', zlabel='Berry curvature', title='Conductance Band', rcount=300, ccount=300)
    end_time = time.time()
    print('运行时间(min)=', (end_time-start_time)/60)

def find_vector_with_the_same_gauge(vector_1, vector_0):
    # 寻找近似的同一的规范
    phase_1_pre = 0
    phase_2_pre = pi
    n_test = 10001
    for i0 in range(n_test):
        test_1 = np.sum(np.abs(vector_1*cmath.exp(1j*phase_1_pre) - vector_0))
        test_2 = np.sum(np.abs(vector_1*cmath.exp(1j*phase_2_pre) - vector_0))
        if test_1 < 1e-9:
            phase = phase_1_pre
            # print('Done with i0=', i0)
            break
        if i0 == n_test-1:
            phase = phase_1_pre
            print('Gauge Not Found with i0=', i0)
        if test_1 < test_2:
            if i0 == 0:
                phase_1 = phase_1_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_1_pre+(phase_2_pre-phase_1_pre)/2
            else:
                phase_1 = phase_1_pre
                phase_2 = phase_1_pre+(phase_2_pre-phase_1_pre)/2
        else:
            if i0 == 0:
                phase_1 = phase_2_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_2_pre+(phase_2_pre-phase_1_pre)/2
            else:
                phase_1 = phase_2_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_2_pre 
        phase_1_pre = phase_1
        phase_2_pre = phase_2
           
    vector_1 = vector_1*cmath.exp(1j*phase)
    # print('二分查找找到的规范=', phase)   
    return vector_1

def plot_3d_surface(x_array, y_array, matrix, xlabel='x', ylabel='y', zlabel='z', title='', fontsize=20, labelsize=15, show=1, save=0, filename='a', file_format='.jpg', dpi=300, z_min=None, z_max=None, rcount=100, ccount=100): 
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    matrix = np.array(matrix)
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    plt.subplots_adjust(bottom=0.1, right=0.65) 
    x_array, y_array = np.meshgrid(x_array, y_array)
    if len(matrix.shape) == 2:
        surf = ax.plot_surface(x_array, y_array, matrix, rcount=rcount, ccount=ccount, cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    elif len(matrix.shape) == 3:
        for i0 in range(matrix.shape[2]):
            surf = ax.plot_surface(x_array, y_array, matrix[:,:,i0], rcount=rcount, ccount=ccount, cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    ax.set_title(title, fontsize=fontsize, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=fontsize, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=fontsize, fontfamily='Times New Roman') 
    ax.set_zlabel(zlabel, fontsize=fontsize, fontfamily='Times New Roman') 
    ax.zaxis.set_major_locator(LinearLocator(5)) 
    ax.zaxis.set_major_formatter('{x:.2f}')  
    if z_min!=None or z_max!=None:
        if z_min==None:
            z_min=matrix.min()
        if z_max==None:
            z_max=matrix.max()
        ax.set_zlim(z_min, z_max)
    ax.tick_params(labelsize=labelsize) 
    labels = ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()
    [label.set_fontname('Times New Roman') for label in labels] 
    cax = plt.axes([0.8, 0.1, 0.05, 0.8]) 
    cbar = fig.colorbar(surf, cax=cax)  
    cbar.ax.tick_params(labelsize=labelsize)
    for l in cbar.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
    if save == 1:
        plt.savefig(filename+file_format, dpi=dpi) 
    if show == 1:
        plt.show()
    plt.close('all')

if __name__ == '__main__':
    main()