"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6075
"""

import kwant
import numpy as np
from matplotlib import pyplot

def make_system():
    a = 1
    lat = kwant.lattice.square(a)
    syst = kwant.Builder()
    t = 1.0
    W = 5
    L = 50
    syst[(lat(x, y) for x in range(L) for y in range(W))] = 0
    syst[lat.neighbors()] = -t  
    #   几何形状如下所示：
    #               lead2         lead3
    #   lead1(L)                          lead4(R)  
    #               lead6         lead5
    lead1 = kwant.Builder(kwant.TranslationalSymmetry((-a, 0)))
    lead1[(lat(0, j) for j in range(W))] = 0
    lead1[lat.neighbors()] = -t
    syst.attach_lead(lead1) 

    lead2 = kwant.Builder(kwant.TranslationalSymmetry((0, -a)))
    lead2[(lat(j, 0) for j in range(W))] = 0
    lead2[lat.neighbors()] = -t  
    syst.attach_lead(lead2) 

    lead3 = kwant.Builder(kwant.TranslationalSymmetry((0, -a)))
    lead3[(lat(j+(L-W), 0) for j in range(W))] = 0
    lead3[lat.neighbors()] = -t  
    syst.attach_lead(lead3) 

    syst.attach_lead(lead1.reversed())   # lead4
    syst.attach_lead(lead3.reversed())   # lead5
    syst.attach_lead(lead2.reversed())   # lead6

    kwant.plot(syst) 
    syst = syst.finalized() 
    return syst


def main():
    syst = make_system()
    energies = np.linspace(-4, 4, 800)
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    for energy in energies:
        smatrix = kwant.smatrix(syst, energy)  
        data1.append(smatrix.transmission(1, 0))   # compute the transmission probability from lead 0 to lead 1
        data2.append(smatrix.transmission(2, 0))
        data3.append(smatrix.transmission(3, 0))
        data4.append(smatrix.transmission(4, 0))
        data5.append(smatrix.transmission(5, 0))
        data6.append(smatrix.transmission(1, 0)+smatrix.transmission(2, 0)+smatrix.transmission(3, 0)+smatrix.transmission(4, 0)+smatrix.transmission(5, 0))
    pyplot.plot(energies, data1)
    pyplot.xlabel("energy [t]")
    pyplot.ylabel("Transmission_12 [e^2/h]")
    pyplot.show()
    pyplot.plot(energies, data2)
    pyplot.xlabel("energy [t]")
    pyplot.ylabel("Transmission_13 [e^2/h]")
    pyplot.show()
    pyplot.plot(energies, data3)
    pyplot.xlabel("energy [t]")
    pyplot.ylabel("Transmission_14 [e^2/h]")
    pyplot.show()
    pyplot.plot(energies, data4)
    pyplot.xlabel("energy [t]")
    pyplot.ylabel("Transmission_15 [e^2/h]")
    pyplot.show()
    pyplot.plot(energies, data5)
    pyplot.xlabel("energy [t]")
    pyplot.ylabel("Transmission_16 [e^2/h]")
    pyplot.show()
    pyplot.plot(energies, data6)
    pyplot.xlabel("energy [t]")
    pyplot.ylabel("Transmission_1_all [e^2/h]")
    pyplot.show()


if __name__ == '__main__':
    main()