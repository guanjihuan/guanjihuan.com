"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/29155
"""

import numpy as np
import matplotlib.pyplot as plt

def get_data(x_array, y_array):
    z_matrix = np.zeros((y_array.shape[0], x_array.shape[0]))
    j0 = -1
    for x in x_array:
        j0 += 1
        i0 = -1
        for y in y_array:
            i0 += 1
            z_matrix[i0, j0] = x**2+y**2
    return z_matrix

x_array = np.linspace(-1, 1, 1000)
y_array = x_array
z_matrix = get_data(x_array, y_array)  # 举例的数据

fix_value = 0.5  # 画这个值附近的等高线
precision = 0.01 # 选取该值附近的范围

# 方法一
x_array_new = []
y_array_new = []
for i0 in range(y_array.shape[0]):
    for j0 in range(x_array.shape[0]):
        if abs(z_matrix[i0, j0]-fix_value)<precision:
            x_array_new.append(x_array[j0])
            y_array_new.append(y_array[i0])
fig, ax = plt.subplots()
plt.plot(x_array_new, y_array_new, 'o')
ax.set_xlim(min(x_array), max(x_array))
ax.set_ylim(min(y_array), max(y_array))
plt.show()

# 方法二
for i0 in range(y_array.shape[0]):
    for j0 in range(x_array.shape[0]):
        if abs(z_matrix[i0, j0]-fix_value)>precision:
            z_matrix[i0, j0] = None
fig, ax = plt.subplots()
ax.contourf(x_array,y_array,z_matrix) 
plt.show()