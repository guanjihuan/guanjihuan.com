"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/15978
"""

import sympy


def main():
    print('bases in the real space')
    a = sympy.symbols('a')
    a1 = sympy.Matrix(1, 2, [3*a/2, sympy.sqrt(3)*a/2])
    a2 = sympy.Matrix(1, 2, [3*a/2, -sympy.sqrt(3)*a/2])
    print('a1:')
    sympy.pprint(a1)
    print('a2:')
    sympy.pprint(a2)
    print('\nbases in the reciprocal space')
    b1, b2 = calculate_two_dimensional_reciprocal_lattice_vectors_with_sympy(a1, a2)
    print('b1:')
    sympy.pprint(b1)
    print('b2:')
    sympy.pprint(b2)


def calculate_one_dimensional_reciprocal_lattice_vector_with_sympy(a1):
    b1 = 2*sympy.pi/a1
    return b1


def calculate_two_dimensional_reciprocal_lattice_vectors_with_sympy(a1, a2):
    a1 = sympy.Matrix(1, 3, [a1[0], a1[1], 0])
    a2 = sympy.Matrix(1, 3, [a2[0], a2[1], 0])
    a3 = sympy.Matrix(1, 3, [0, 0, 1])
    cross_a2_a3 = a2.cross(a3)
    cross_a3_a1 = a3.cross(a1)
    b1 = 2*sympy.pi*cross_a2_a3/a1.dot(cross_a2_a3)
    b2 = 2*sympy.pi*cross_a3_a1/a1.dot(cross_a2_a3)
    b1 = sympy.Matrix(1, 2, [b1[0], b1[1]])
    b2 = sympy.Matrix(1, 2, [b2[0], b2[1]])
    return b1, b2


def calculate_three_dimensional_reciprocal_lattice_vectors_with_sympy(a1, a2, a3):
    cross_a2_a3 = a2.cross(a3)
    cross_a3_a1 = a3.cross(a1)
    cross_a1_a2 = a1.cross(a2)
    b1 = 2*sympy.pi*cross_a2_a3/a1.dot(cross_a2_a3)
    b2 = 2*sympy.pi*cross_a3_a1/a1.dot(cross_a2_a3)
    b3 = 2*sympy.pi*cross_a1_a2/a1.dot(cross_a2_a3)
    return b1, b2, b3


if __name__ == '__main__':
    main()