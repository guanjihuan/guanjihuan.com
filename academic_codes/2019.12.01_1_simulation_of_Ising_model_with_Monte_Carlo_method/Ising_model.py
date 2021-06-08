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
    T = 2  # 温度
    ising = get_one_sample(sizeOfSample=size, temperature=T)  # 得到符合玻尔兹曼分布的ising模型
    plot(ising)  # 画图
    energy_s = []
    for i in range(size):
        for j in range(size):
            energy_s0 = getEnergy(i=i, j=j, S=ising)  # 获取格点的能量
            energy_s = np.append(energy_s, [energy_s0], axis=0)
    plt.hist(energy_s, bins=50, density=1, facecolor='red', alpha=0.7)  # 画出格点能量分布  # bins是分布柱子的个数，density是归一化，后面两个参数是管颜色的
    plt.show()


def get_one_sample(sizeOfSample, temperature):
    S = 2 * np.pi * np.random.random(size=(sizeOfSample, sizeOfSample))  # 随机初始状态，角度是0到2pi
    print('体系大小：', S.shape)
    initialEnergy = calculateAllEnergy(S)  # 计算随机初始状态的能量
    print('系统的初始能量是:', initialEnergy)
    newS = np.array(copy.deepcopy(S))
    for i00 in range(1000):  # 循环一定次数，得到平衡的抽样分布
        newS = Metropolis(newS, temperature)  # Metropolis方法抽样，得到玻尔兹曼分布的样品体系
        newEnergy = calculateAllEnergy(newS)
        if np.mod(i00, 100) == 0:
            print('循环次数%i, 当前系统能量是:' % (i00+1), newEnergy)
    print('循环次数%i, 当前系统能量是:' % (i00 + 1), newEnergy)
    return newS


def Metropolis(S, T):  # S是输入的初始状态， T是温度
    delta_max = 0.5 * np.pi # 角度最大的变化度数，默认是90度，也可以调整为其他
    k = 1  # 玻尔兹曼常数
    for i in range(S.shape[0]):
        for j in range(S.shape[0]):
            delta = (2 * np.random.random() - 1) * delta_max   # 角度变化在-90度到90度之间
            newAngle = S[i, j] + delta  # 新角度
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


def plot(S):  # 画图
    X, Y = np.meshgrid(np.arange(0, S.shape[0]), np.arange(0, S.shape[0]))
    U = np.cos(S)
    V = np.sin(S)
    plt.figure()
    plt.quiver(X, Y, U, V, units='inches')
    plt.show()


if __name__ == '__main__':
    main()

