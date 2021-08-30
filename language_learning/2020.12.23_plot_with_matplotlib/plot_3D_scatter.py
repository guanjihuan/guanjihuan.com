import numpy as np
# import os
# os.chdir('D:/data')  # 设置文件保存的位置


def main():
    x = [1, 3, 5, 7]
    y = [2, 4, 6, 8]
    z = [2, 8, 6, 1]
    value = [3, 1, 10, 2]
    Plot_3D_Scatter(x, y, z, value, title='Plot 3D Scatter')


def Plot_3D_Scatter(x, y, z, value, xlabel='x', ylabel='y', zlabel='z', title='title', filename='a'):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LinearLocator
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.1, right=0.8) 
    for i in range(np.array(x).shape[0]):
        ax.scatter(x[i], y[i], z[i], marker='o', s=int(100*value[i]), c=[(1,0,0)])
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_zlabel(zlabel, fontsize=20, fontfamily='Times New Roman') 
    # ax.set_zlim(0, 20) 
    # ax.zaxis.set_major_locator(LinearLocator(6)) # 设置z轴主刻度的个数
    # ax.zaxis.set_major_formatter('{x:.0f}')   # 设置z轴主刻度的格式
    ax.tick_params(labelsize=15)  # 设置刻度值字体大小
    labels = ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()
    [label.set_fontname('Times New Roman') for label in labels] # 设置刻度值字体
    # plt.savefig(filename+'.jpg', dpi=300) 
    plt.show()
    plt.close('all')


if __name__ == '__main__':
    main()