import numpy as np
# import os
# os.chdir('D:/data')  # 设置文件保存的位置


def main():
    x = np.arange(-5, 5, 0.25)
    y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    Plot_3D_Surface(x,y,Z)


def Plot_3D_Surface(x,y,matrix,filename='a.jpg', titlename='Plot 3D Surface'):
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    plt.subplots_adjust(bottom=0.1, right=0.65)  # 调整位置
    x, y = np.meshgrid(x, y)
    surf = ax.plot_surface(x, y, matrix, cmap=cm.coolwarm, linewidth=0, antialiased=False)  # Plot the surface.
    ax.set_title(titlename, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel('x', fontsize=30, fontfamily='Times New Roman') # 坐标标签
    ax.set_ylabel('y', fontsize=30, fontfamily='Times New Roman') # 坐标标签
    ax.set_zlabel('z', fontsize=30, fontfamily='Times New Roman') # 坐标标签
    # ax.set_zlim(-1, 1)  # 设置z轴的范围
    ax.zaxis.set_major_locator(LinearLocator(5)) # 设置z轴主刻度的个数
    ax.zaxis.set_major_formatter('{x:.2f}')   # 设置z轴主刻度的格式
    ax.tick_params(labelsize=15)  # 设置刻度值字体大小
    labels = ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()
    [label.set_fontname('Times New Roman') for label in labels] # 设置刻度值字体
    cax = plt.axes([0.75, 0.15, 0.05, 0.75]) # color bar的位置 [左，下，宽度， 高度]
    cbar = fig.colorbar(surf, cax=cax)  # color bar
    cbar.ax.tick_params(labelsize=15) # 设置color bar刻度的字体大小
    for l in cbar.ax.yaxis.get_ticklabels(): # 设置color bar刻度的字体
        l.set_family('Times New Roman')
    # plt.savefig(filename, dpi=800) # 保存图片文件
    plt.show()
    plt.close('all')  # 关闭所有plt，防止循环画图时占用内存


if __name__ == '__main__':
    main()