# 波函数规范的选取
import numpy as np
import cmath
import guan

# Fixed gauge example 1
vector = np.array([np.sqrt(0.5), np.sqrt(0.5)])*cmath.exp(np.random.uniform(0, 1)*1j)
print('\nExample 1\n', vector)
print(np.dot(vector.transpose().conj(), vector), '\n')

vector = guan.find_vector_with_fixed_gauge_by_making_one_component_real(vector)
print(vector)
print(np.dot(vector.transpose().conj(), vector), '\n')

# Fixed gauge example 2
vector = np.array([1, 0])*cmath.exp(np.random.uniform(0, 1)*1j)
print('\nExample 2\n', vector)
print(np.dot(vector.transpose().conj(), vector), '\n')

vector = guan.find_vector_with_fixed_gauge_by_making_one_component_real(vector)
print(vector)
print(np.dot(vector.transpose().conj(), vector), '\n')