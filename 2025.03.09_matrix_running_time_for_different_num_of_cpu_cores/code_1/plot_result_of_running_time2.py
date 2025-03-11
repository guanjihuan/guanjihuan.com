import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

cpu_num_array = np.arange(1, 17)



# n = 30000

time_array_1 = [1164.522, 648.587, 444.488, 647.176, 298.652, 256.809, 239.630, 231.987, 475.781, 383.823, 410.388, 172.702, 163.727, 144.307, 121.530, 109.636]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.show()

time_0 = time_array_1[0]
for i0 in range(len(time_array_1)):
    time_array_1[i0] = time_0/time_array_1[i0]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.show()




# n = 20000

time_array_1 = [365.730, 209.475, 151.805, 120.739, 104.102, 88.944, 80.475, 70.486, 67.500, 61.404, 53.837, 51.219, 51.542, 84.641, 80.378, 30.629]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.show()

time_0 = time_array_1[0]
for i0 in range(len(time_array_1)):
    time_array_1[i0] = time_0/time_array_1[i0]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.show()




# n = 10000

time_array_1 = [62.485, 36.402, 25.316, 21.785, 17.619, 15.412, 16.718, 10.874, 9.588, 7.004, 6.733, 7.251, 7.248, 4.979, 4.889, 7.037]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.show()

time_0 = time_array_1[0]
for i0 in range(len(time_array_1)):
    time_array_1[i0] = time_0/time_array_1[i0]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.show()




# n = 500

time_array_1 = [0.004053801, 0.002605676, 0.001590664, 0.001103345, 0.001266495, 0.000954730, 0.000930616, 0.000779754, 0.000970088, 0.000651353, 0.000918634, 0.000538209, 0.000716934, 0.000521487, 0.001165715, 0.000764804 ]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.show()

time_0 = time_array_1[0]
for i0 in range(len(time_array_1)):
    time_array_1[i0] = time_0/time_array_1[i0]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.show()




# n = 300

time_array_1 = [0.001144045, 0.000554059, 0.000413136, 0.000385368, 0.000287431, 0.000270178, 0.000268842, 0.000535453, 0.000219275, 0.000219676, 0.000186116, 0.000522058, 0.000146788, 0.000134041, 0.000558532, 0.000135554]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.show()

time_0 = time_array_1[0]
for i0 in range(len(time_array_1)):
    time_array_1[i0] = time_0/time_array_1[i0]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.show()




# n = 100

time_array_1 = [0.000041899, 0.000104283, 0.000138595, 0.000038628, 0.000039540, 0.000029726, 0.000101140, 0.000023468, 0.000061134, 0.000225034, 0.000033439, 0.000075225, 0.000057184, 0.000040229, 0.000104894, 0.000041510]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.show()

time_0 = time_array_1[0]
for i0 in range(len(time_array_1)):
    time_array_1[i0] = time_0/time_array_1[i0]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.show()