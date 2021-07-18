import guan
import sympy

a1 = [0, 1]
a2 = [1, 0]
b1, b2 = guan.calculate_two_dimensional_reciprocal_lattice_vectors(a1, a2)
print(b1, b2, '\n')

print('bases in the real space')
a = sympy.symbols('a')
a1 = sympy.Matrix(1, 2, [3*a/2, sympy.sqrt(3)*a/2])
a2 = sympy.Matrix(1, 2, [3*a/2, -sympy.sqrt(3)*a/2])
print('a1:')
sympy.pprint(a1)
print('a2:')
sympy.pprint(a2)
print('\nbases in the reciprocal space')
b1, b2 = guan.calculate_two_dimensional_reciprocal_lattice_vectors_with_sympy(a1, a2)
print('b1:')
sympy.pprint(b1)
print('b2:')
sympy.pprint(b2)