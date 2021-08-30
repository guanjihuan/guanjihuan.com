"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/8734

函数调用目录：
1. x, y = read_one_dimensional_data(filename='a')
2. x, y, matrix = read_two_dimensional_data(filename='a')
3. write_one_dimensional_data(x, y, filename='a')
4. write_two_dimensional_data(x, y, matrix, filename='a')
5. plot(x, y, xlabel='x', ylabel='y', title='', filename='a')
6. plot_3d_surface(x, y, matrix, xlabel='x', ylabel='y', zlabel='z', title='', filename='a')
7. plot_contour(x, y, matrix, xlabel='x', ylabel='y', title='', filename='a')
8. plot_2d_scatter(x, y, value, xlabel='x', ylabel='y', title='', filename='a')
9. plot_3d_surface(x, y, z, value, xlabel='x', ylabel='y', zlabel='z', title='', filename='a')
10. creat_animation(image_names, duration_time=0.5, filename='a')
11. eigenvalue_array = calculate_eigenvalue_with_one_paramete(x, matrix)
12. eigenvalue_array = calculate_eigenvalue_with_two_parameters(x, y, matrix)

函数对应的功能：
1. 读取filename.txt文件中的一维数据y(x)
2. 读取filename.txt文件中的二维数据matrix(x,y)
3. 把一维数据y(x)写入filename.txt文件  
4. 把二维数据matrix(x,y)写入filename.txt文件
5. 画y(x)图，并保存到filename.jpg文件。具体画图格式可在函数中修改！
6. 画3d_surface图，并保存到filename.jpg文件。具体画图格式可在函数中修改！
7. 画contour图，并保存到filename.jpg文件。具体画图格式可在函数中修改！
8. 画2d_scatter图，并保存到filename.jpg文件。具体画图格式可在函数中修改！
9. 画3d_scatter图，并保存到filename.jpg文件。具体画图格式可在函数中修改！
10. 制作动画
11. 在参数x下，计算matrix函数的本征值eigenvalue_array[:, index]
12. 在参数(x,y)下，计算matrix函数的本征值eigenvalue_array[:, :, index]
"""


import numpy as np
# import os
# os.chdir('D:/data')


def main():
    pass  # 读取数据 + 数据处理 + 保存新数据


# 1. 读取filename.txt文件中的一维数据y(x)  
def read_one_dimensional_data(filename='a'): 
    f = open(filename+'.txt', 'r')
    text = f.read()
    f.close()
    row_list = np.array(text.split('\n')) 
    dim_column = np.array(row_list[0].split()).shape[0] 
    x = np.array([])
    y = np.array([])
    for row in row_list:
        column = np.array(row.split()) 
        if column.shape[0] != 0:  
            x = np.append(x, [float(column[0])], axis=0)  
            y_row = np.zeros(dim_column-1)
            for dim0 in range(dim_column-1):
                y_row[dim0] = float(column[dim0+1])
            if np.array(y).shape[0] == 0:
                y = [y_row]
            else:
                y = np.append(y, [y_row], axis=0)
    return x, y


# 2. 读取filename.txt文件中的二维数据matrix(x,y)  
def read_two_dimensional_data(filename='a'): 
    f = open(filename+'.txt', 'r')
    text = f.read()
    f.close()
    row_list = np.array(text.split('\n')) 
    dim_column = np.array(row_list[0].split()).shape[0] 
    x = np.array([])
    y = np.array([])
    matrix = np.array([])
    for i0 in range(row_list.shape[0]):
        column = np.array(row_list[i0].split()) 
        if i0 == 0:
            x_str = column[1::] 
            x = np.zeros(x_str.shape[0])
            for i00 in range(x_str.shape[0]):
                x[i00] = float(x_str[i00]) 
        elif column.shape[0] != 0: 
            y = np.append(y, [float(column[0])], axis=0)  
            matrix_row = np.zeros(dim_column-1)
            for dim0 in range(dim_column-1):
                matrix_row[dim0] = float(column[dim0+1])
            if np.array(matrix).shape[0] == 0:
                matrix = [matrix_row]
            else:
                matrix = np.append(matrix, [matrix_row], axis=0)
    return x, y, matrix


# 3. 把一维数据y(x)写入filename.txt文件  
def write_one_dimensional_data(x, y, filename='a'): 
    with open(filename+'.txt', 'w') as f:
        i0 = 0
        for x0 in x:
            f.write(str(x0)+'   ')
            if len(y.shape) == 1:
                f.write(str(y[i0])+'\n')
            elif len(y.shape) == 2:
                for j0 in range(y.shape[1]):
                    f.write(str(y[i0, j0])+'   ')
                f.write('\n')
            i0 += 1


# 4. 把二维数据matrix(x,y)写入filename.txt文件  
def write_two_dimensional_data(x, y, matrix, filename='a'): 
    with open(filename+'.txt', 'w') as f:
        f.write('0   ')
        for x0 in x:
            f.write(str(x0)+'   ')
        f.write('\n')
        i0 = 0
        for y0 in y:
            f.write(str(y0))
            j0 = 0
            for x0 in x:
                f.write('   '+str(matrix[i0, j0])+'   ')
                j0 += 1
            f.write('\n')
            i0 += 1   


# 5. 画y(x)图，并保存到filename.jpg文件。具体画图格式可在函数中修改。
def plot(x, y, xlabel='x', ylabel='y', title='', filename='a', show=1, save=0): 
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.20, left=0.18) 
    ax.plot(x, y, '-o')
    ax.grid()
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.tick_params(labelsize=20) 
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    if save == 1:
        plt.savefig(filename+'.jpg', dpi=300) 
    if show == 1:
        plt.show()
    plt.close('all')



# 6. 画3d_surface图，并保存到filename.jpg文件。具体画图格式可在函数中修改。
def plot_3d_surface(x, y, matrix, xlabel='x', ylabel='y', zlabel='z', title='', filename='a', show=1, save=0): 
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    plt.subplots_adjust(bottom=0.1, right=0.65) 
    x, y = np.meshgrid(x, y)
    if len(matrix.shape) == 2:
        surf = ax.plot_surface(x, y, matrix, cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    elif len(matrix.shape) == 3:
        for i0 in range(matrix.shape[2]):
            surf = ax.plot_surface(x, y, matrix[:,:,i0], cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_zlabel(zlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.zaxis.set_major_locator(LinearLocator(5)) 
    ax.zaxis.set_major_formatter('{x:.2f}')   
    ax.tick_params(labelsize=15) 
    labels = ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()
    [label.set_fontname('Times New Roman') for label in labels] 
    cax = plt.axes([0.80, 0.15, 0.05, 0.75]) 
    cbar = fig.colorbar(surf, cax=cax)  
    cbar.ax.tick_params(labelsize=15)
    for l in cbar.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
    if save == 1:
        plt.savefig(filename+'.jpg', dpi=300) 
    if show == 1:
        plt.show()
    plt.close('all')



# 7. 画plot_contour图，并保存到filename.jpg文件。具体画图格式可在函数中修改。
def plot_contour(x, y, matrix, xlabel='x', ylabel='y', title='', filename='a', show=1, save=0):  
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2, right=0.75, left = 0.16) 
    x, y = np.meshgrid(x, y)
    contour = ax.contourf(x,y,matrix,cmap='jet') 
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.tick_params(labelsize=15) 
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels] 
    cax = plt.axes([0.78, 0.17, 0.08, 0.71])
    cbar = fig.colorbar(contour, cax=cax) 
    cbar.ax.tick_params(labelsize=15) 
    for l in cbar.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
    if save == 1:
        plt.savefig(filename+'.jpg', dpi=300) 
    if show == 1:
        plt.show()
    plt.close('all')


# 8. 画2d_scatter图，并保存到filename.jpg文件。具体画图格式可在函数中修改！
def plot_2d_scatter(x, y, value, xlabel='x', ylabel='y', title='', filename='a', show=1, save=0):
    import matplotlib.pyplot as plt
    from matplotlib.axes._axes import _log as matplotlib_axes_logger
    matplotlib_axes_logger.setLevel('ERROR') 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.subplots_adjust(bottom=0.2, right=0.8, left=0.2) 
    for i in range(np.array(x).shape[0]):
        ax.scatter(x[i], y[i], marker='o', s=100*value[i], c=(1,0,0))
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.tick_params(labelsize=15)
    labels = ax.get_xticklabels() + ax.get_yticklabels() 
    [label.set_fontname('Times New Roman') for label in labels]
    if save == 1:
        plt.savefig(filename+'.jpg', dpi=300) 
    if show == 1:
        plt.show()
    plt.close('all')


# 9. 画3d_scatter图，并保存到filename.jpg文件。具体画图格式可在函数中修改！
def plot_3d_scatter(x, y, z, value, xlabel='x', ylabel='y', zlabel='z', title='', filename='a', show=1, save=0):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LinearLocator
    from matplotlib.axes._axes import _log as matplotlib_axes_logger
    matplotlib_axes_logger.setLevel('ERROR')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.1, right=0.8) 
    for i in range(np.array(x).shape[0]):
        ax.scatter(x[i], y[i], z[i], marker='o', s=int(100*value[i]), c=(1,0,0))
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_zlabel(zlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.tick_params(labelsize=15) 
    labels = ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    if save == 1:
        plt.savefig(filename+'.jpg', dpi=300) 
    if show == 1:
        plt.show()
    plt.close('all')


# 10. 制作动画
def creat_animation(image_names, duration_time=0.5, filename='a'):  
    import imageio
    images = []
    for name in image_names:
        image = name+'.jpg'
        im = imageio.imread(image)
        images.append(im)
    imageio.mimsave(filename+'.gif', images, 'GIF', duration=duration_time)  # durantion是延迟时间


# 11. 在参数x下，计算matrix函数的本征值eigenvalue_array[:, index]
def calculate_eigenvalue_with_one_parameter(x, matrix):
    dim_x = np.array(x).shape[0]
    i0 = 0
    if np.array(matrix(0)).shape==():
        eigenvalue_array = np.zeros((dim_x, 1))
        for x0 in x:
            matrix0 = matrix(x0)
            eigenvalue_array[i0, 0] = np.real(matrix0)
            i0 += 1
    else:
        dim = np.array(matrix(0)).shape[0]
        eigenvalue_array = np.zeros((dim_x, dim))
        for x0 in x:
            matrix0 = matrix(x0)
            eigenvalue, eigenvector = np.linalg.eig(matrix0)
            eigenvalue_array[i0, :] = np.sort(np.real(eigenvalue[:]))
            i0 += 1
    return eigenvalue_array


# 12. 在参数(x,y)下，计算matrix函数的本征值eigenvalue_array[:, :, index]
def calculate_eigenvalue_with_two_parameters(x, y, matrix):  
    dim_x = np.array(x).shape[0]
    dim_y = np.array(y).shape[0]
    if np.array(matrix(0,0)).shape==():
        eigenvalue_array = np.zeros((dim_y, dim_x, 1))
        i0 = 0
        for y0 in y:
            j0 = 0
            for x0 in x:
                matrix0 = matrix(x0, y0)
                eigenvalue_array[i0, j0, 0] = np.real(matrix0)
                j0 += 1
            i0 += 1
    else:
        dim = np.array(matrix(0, 0)).shape[0]
        eigenvalue_array = np.zeros((dim_y, dim_x, dim))
        i0 = 0
        for y0 in y:
            j0 = 0
            for x0 in x:
                matrix0 = matrix(x0, y0)
                eigenvalue, eigenvector = np.linalg.eig(matrix0)
                eigenvalue_array[i0, j0, :] = np.sort(np.real(eigenvalue[:]))
                j0 += 1
            i0 += 1
    return eigenvalue_array


if __name__ == "__main__":
    main()