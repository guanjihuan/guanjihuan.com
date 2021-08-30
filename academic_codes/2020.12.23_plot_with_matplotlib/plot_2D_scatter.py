import numpy as np
# import os
# os.chdir('D:/data')  # 设置文件保存的位置


def main():
    x = [4, 3, 5, 7]
    y = [6, 1, 3, 2]
    value = [3, 1, 10, 2]
    Plot_2D_Scatter(x, y, value, title='Plot 2D Scatter')


def Plot_2D_Scatter(x, y, value, xlabel='x', ylabel='y', title='title', filename='a'):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.subplots_adjust(bottom=0.2, right=0.8, left=0.2) 
    for i in range(np.array(x).shape[0]):
        ax.scatter(x[i], y[i], marker='o', s=100*value[i], c=[(1,0,0)])
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.tick_params(labelsize=15)  # 设置刻度值字体大小
    labels = ax.get_xticklabels() + ax.get_yticklabels() 
    [label.set_fontname('Times New Roman') for label in labels] # 设置刻度值字体
    # plt.savefig(filename+'.jpg', dpi=300) 
    plt.show()
    plt.close('all')


if __name__ == '__main__':
    main()