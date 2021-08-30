import numpy as np
# import os
# os.chdir('D:/data')  # 设置路径


def main():  
    x1, x2, matrix = read_two_dimension('2D_data.txt')
    plot_matrix(x1, x2, matrix)


def read_two_dimension(file_name):
    f = open(file_name, 'r')
    text = f.read()
    f.close()
    row_list = np.array(text.split('\n'))  # 根据“回车”分割成每一行
    # print('文本格式：')
    # print(text)
    # print('row_list:')
    # print(row_list)
    # print('column:')
    dim_column = np.array(row_list[0].split()).shape[0] # 列数
    x1 = np.array([])
    x2 = np.array([])
    matrix = np.array([])
    for i0 in range(row_list.shape[0]):
        column = np.array(row_list[i0].split())  # 每一行根据“空格”继续分割
        # print(column)
        if i0 == 0:
            x1_str = column[1::]  # x1坐标（去除第一个在角落的值）
            x1 = np.zeros(x1_str.shape[0])
            for i00 in range(x1_str.shape[0]):
                x1[i00] = float(x1_str[i00])  # 字符串转浮点
        elif column.shape[0] != 0:  # 解决最后一行空白的问题
            x2 = np.append(x2, [float(column[0])], axis=0)  # 第一列为x数据
            matrix_row = np.zeros(dim_column-1)
            for dim0 in range(dim_column-1):
                matrix_row[dim0] = float(column[dim0+1])
            if np.array(matrix).shape[0] == 0:
                matrix = [matrix_row]
            else:
                matrix = np.append(matrix, [matrix_row], axis=0)
    # print('x1:')
    # print(x1)
    # print('x2:')
    # print(x2)
    # print('matrix:')
    # print(matrix)
    return x1, x2, matrix



def plot_matrix(x1, x2, matrix):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x1, x2 = np.meshgrid(x1, x2)
    ax.plot_surface(x1, x2, matrix, cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    plt.xlabel('x1')
    plt.ylabel('x2') 
    ax.set_zlabel('z')  
    plt.show()



if __name__ == '__main__': 
    main()