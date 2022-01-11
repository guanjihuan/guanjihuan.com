"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/3888
"""

import kwant


def make_system():
    a = 1
    lat = kwant.lattice.square(a, norbs=1)  # 创建晶格，方格子
    syst = kwant.Builder() 
    t = 1.0
    W = 60  # 中心体系宽度
    L = 100  # 中心体系长度
    # 给中心体系赋值
    for i in range(L):
        for j in range(W):
            syst[lat(i, j)] = 0
            if j > 0:
                syst[lat(i, j), lat(i, j-1)] = -t  # hopping in y-direction
            if i > 0:
                syst[lat(i, j), lat(i-1, j)] = -t  # hopping in x-direction
            if 47<=i<53 and 27<=j<33:  # 势垒
                syst[lat(i, j)] = 1e8
    # 电极
    lead = kwant.Builder(kwant.TranslationalSymmetry((-a, 0)))
    lead[(lat(0, j) for j in range(W))] = 0
    lead[lat.neighbors()] = -t  # 用neighbors()方法
    syst.attach_lead(lead)  # 左电极
    syst.attach_lead(lead.reversed())   # 用reversed()方法得到右电极
    # 制作结束
    kwant.plot(syst) 
    syst = syst.finalized()  
    return syst


def main():
    syst = make_system()
    psi = kwant.wave_function(syst)(0)[29]
    current = kwant.operator.Current(syst)(psi)
    kwant.plotter.current(syst, current)


if __name__ == '__main__':
    main()