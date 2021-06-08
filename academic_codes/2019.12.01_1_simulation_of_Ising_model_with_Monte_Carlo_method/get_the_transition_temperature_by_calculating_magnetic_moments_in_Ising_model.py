"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/1249
"""

import random
import matplotlib.pyplot as plt
import numpy as np
import copy
import math
import time


def main():
    size = 30  # 体系大小
    for T in np.linspace(0.02, 5, 100):
        ising, magnetism = get_one_sample(sizeOfSample=size, temperature=T)
        print('温度=', T, '   磁矩=', magnetism, '   总能量=', calculateAllEnergy(ising))
        plt.plot(T, magnetism, 'o')
    plt.show()


def get_one_sample(sizeOfSample, temperature):
    newS = np.zeros((sizeOfSample, sizeOfSample))  # 初始状态
    magnetism = 0
    for i00 in range(100):
        newS = Metropolis(newS, temperature)
        magnetism = magnetism + abs(sum(sum(np.cos(newS))))/newS.shape[0]**2
    magnetism = magnetism/100
    return newS, magnetism


def Metropolis(S, T):  # S是输入的初始状态， T是温度
    k = 1  # 玻尔兹曼常数
    for i in range(S.shape[0]):
        for j in range(S.shape[0]):
            newAngle = np.random.randint(-1, 1)*np.pi
            energyBefore = getEnergy(i=i, j=j, S=S, angle=None)  # 获取该格点的能量
            energyLater = getEnergy(i=i, j=j, S=S, angle=newAngle)  # 获取格点变成新角度时的能量
            alpha = min(1.0, math.exp(-(energyLater - energyBefore)/(k * T)))  # 这个接受率对应的是玻尔兹曼分布
            if random.uniform(0, 1) <= alpha:
                S[i, j] = newAngle   # 接受新状态
            else:
                pass  # 保持为上一个状态
    return S


def getEnergy(i, j, S, angle=None):  # 计算(i,j)位置的能量，为周围四个的相互能之和
    width = S.shape[0]
    height = S.shape[1]
    top_i = i - 1 if i > 0 else width - 1  # 用到周期性边界条件
    bottom_i = i + 1 if i < (width - 1) else 0
    left_j = j - 1 if j > 0 else height - 1
    right_j = j + 1 if j < (height - 1) else 0
    environment = [[top_i, j], [bottom_i, j], [i, left_j], [i, right_j]]
    energy = 0
    if angle == None:
        for num_i in range(4):
            energy += -np.cos(S[i, j] - S[environment[num_i][0], environment[num_i][1]])
    else:
        for num_i in range(4):
            energy += -np.cos(angle - S[environment[num_i][0], environment[num_i][1]])
    return energy


def calculateAllEnergy(S):  # 计算整个体系的能量
    energy = 0
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            energy += getEnergy(i, j, S)
    return energy/2  # 作用两次要减半


if __name__ == '__main__':
    main()

