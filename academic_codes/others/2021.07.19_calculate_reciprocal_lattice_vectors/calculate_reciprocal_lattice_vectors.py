"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/15978
"""

import numpy as np
from math import *

def main():
    a1 = [0, 1]
    a2 = [1, 0]
    b1, b2 = calculate_two_dimensional_reciprocal_lattice_vectors(a1, a2)
    print(b1, b2)


def calculate_one_dimensional_reciprocal_lattice_vector(a1):
    b1 = 2*pi/a1
    return b1


def calculate_two_dimensional_reciprocal_lattice_vectors(a1, a2):
    a1 = np.array(a1)
    a2 = np.array(a2)
    a1 = np.append(a1, 0)
    a2 = np.append(a2, 0)
    a3 = np.array([0, 0, 1])
    b1 = 2*pi*np.cross(a2, a3)/np.dot(a1, np.cross(a2, a3))
    b2 = 2*pi*np.cross(a3, a1)/np.dot(a1, np.cross(a2, a3))
    b1 = np.delete(b1, 2)
    b2 = np.delete(b2, 2)
    return b1, b2


def calculate_three_dimensional_reciprocal_lattice_vectors(a1, a2, a3):
    a1 = np.array(a1)
    a2 = np.array(a2)
    a3 = np.array(a3)
    b1 = 2*pi*np.cross(a2, a3)/np.dot(a1, np.cross(a2, a3))
    b2 = 2*pi*np.cross(a3, a1)/np.dot(a1, np.cross(a2, a3))
    b3 = 2*pi*np.cross(a1, a2)/np.dot(a1, np.cross(a2, a3))
    return b1, b2, b3


if __name__ == '__main__':
    main()