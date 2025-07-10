# 循环参数计算

import guan
import numpy as np

def test_1(x):
    return 2*x

x_array = np.arange(0, 5, 1)
result_array = guan.loop_calculation_with_one_parameter(test_1, x_array)
print(result_array)
guan.plot(x_array, result_array)
print()

def test_2(x, y):
    return x+y

x_array = np.arange(0, 5, 1)
y_array = np.arange(0, 3, 1)
result_array = guan.loop_calculation_with_two_parameters(test_2, x_array, y_array)
print(result_array)
guan.plot_contour(x_array, y_array, result_array)
print()

def test_3(x, y, z):
    return x+y+z

x_array = np.arange(0, 5, 1)
y_array = np.arange(0, 3, 1)
z_array = np.arange(0, 2, 1)
result_array = guan.loop_calculation_with_three_parameters(test_3, x_array, y_array, z_array)
print(result_array)
guan.plot_contour(y_array, z_array, result_array[:, :, 4])