"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/10909
"""

import numpy as np


def main():
    x_array = np.arange(-5, 5.1)
    y_array = np.arange(-5, 5.1)
    coordinates = []
    for x in x_array:
        for y in y_array:
            coordinates.append([x, y])
    plot_dots(coordinates)


def plot_dots(coordinates):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9,9))
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    plt.axis('off')
    for i1 in range(len(coordinates)):
        for i2 in range(len(coordinates)):
            if np.sqrt((coordinates[i1][0] - coordinates[i2][0])**2+(coordinates[i1][1] - coordinates[i2][1])**2) < 1.1:
                ax.plot([coordinates[i1][0], coordinates[i2][0]], [coordinates[i1][1], coordinates[i2][1]], '-k', linewidth=1)
    for i in range(len(coordinates)):
        ax.plot(coordinates[i][0], coordinates[i][1], 'ro', markersize=10)
    # plt.savefig('square.eps') 
    plt.show()


if __name__ == '__main__':
    main()