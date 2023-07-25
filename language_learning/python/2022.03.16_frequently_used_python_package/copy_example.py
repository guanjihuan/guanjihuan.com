import copy
import numpy as np

array_1 = [1, 2, 3]
array_2 = array_1
array_1[0] = 100
print('array_1=', array_1)
print('array_2=', array_2, '\n')

array_1 = np.array([1, 2, 3])
array_2 = array_1
array_1[0] = 100
print('array_1=', array_1)
print('array_2=', array_2, '\n')

array_1 = [1, 2, 3]
array_2 = copy.deepcopy(array_1)
array_1[0] = 100
print('array_1=', array_1)
print('array_2=', array_2, '\n')

array_1 = np.array([1, 2, 3])
array_2 = copy.deepcopy(array_1)
array_1[0] = 100
print('array_1=', array_1)
print('array_2=', array_2)