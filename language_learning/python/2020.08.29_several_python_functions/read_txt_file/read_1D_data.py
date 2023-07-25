import numpy as np  
import matplotlib.pyplot as plt
# import os
# os.chdir('D:/data')  # 设置路径


def main():  
    x, y = read_one_dimension('1D_data.txt')
    for dim0 in range(y.shape[1]):
        plt.plot(x, y[:, dim0], '-k')
    plt.show()


def read_one_dimension(file_name):
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
    x = np.array([])
    y = np.array([])
    for row in row_list:
        column = np.array(row.split())  # 每一行根据“空格”继续分割
        # print(column)
        if column.shape[0] != 0:  # 解决最后一行空白的问题
            x = np.append(x, [float(column[0])], axis=0)  # 第一列为x数据
            y_row = np.zeros(dim_column-1)
            for dim0 in range(dim_column-1):
                y_row[dim0] = float(column[dim0+1])
            if np.array(y).shape[0] == 0:
                y = [y_row]
            else:
                y = np.append(y, [y_row], axis=0)
    # print('x:')
    # print(x)
    # print('y:')
    # print(y)
    return x, y


if __name__ == '__main__': 
    main()