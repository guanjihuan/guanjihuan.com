import numpy as np
# import os
# os.chdir('D:/data')  # 设置文件保存的位置


def main():
    x = np.arange(0.0, 2.0, 0.01)
    y = 1 + np.sin(2 * np.pi * x)
    Plot_Line(x,y)


def Plot_Line(x,y,filename='a.jpg', titlename='Plot Line'):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.20, left=0.16) 
    ax.plot(x, y, '-o')
    ax.grid()
    ax.set_title(titlename, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel('x', fontsize=30, fontfamily='Times New Roman') # 坐标标签
    ax.set_ylabel('y', fontsize=30, fontfamily='Times New Roman') # 坐标标签
    ax.tick_params(labelsize=20)  # 设置刻度值字体大小
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels] # 设置刻度值字体
    # plt.savefig(filename, dpi=800) # 保存图片文件
    plt.show()
    plt.close('all')  # 关闭所有plt，防止循环画图时占用内存


if __name__ == '__main__':
    main()