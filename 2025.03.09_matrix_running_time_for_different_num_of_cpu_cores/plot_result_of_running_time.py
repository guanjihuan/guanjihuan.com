import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

cpu_num_array = np.arange(1, 17)

time_array_1 = [3.999, 1.679, 1.257, 0.985, 0.699, 0.562, 0.534, 0.525, 0.510, 0.424, 0.409, 0.380, 0.372, 0.339, 0.334, 0.293]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.show()

time_array_2 = [6.059, 2.723, 2.190, 1.577, 1.169, 0.939, 1.231, 0.958, 1.070, 0.793, 1.208, 0.760, 0.709, 0.677, 0.671, 0.906]
fig, ax = plt.subplots()
ax.set_title('np.linalg.inv()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_2, '-o', )
plt.show()

time_array_3 = [95.896, 49.107, 41.703, 38.915, 32.468, 25.804, 40.716, 31.072, 40.045, 26.397, 38.557, 28.684, 28.267, 26.840, 27.381, 34.494]
fig, ax = plt.subplots()
ax.set_title('np.linalg.eig()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_3, '-o', )
plt.show()