import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator
import numpy as np
import pickle

cpu_num_array = np.arange(1, 65)

n = 1000

time_array_1 = []
for cpu_num in cpu_num_array:
    with open(f'./task_{cpu_num}/multiply_time_n={n}.pkl', 'rb') as f:
        data = pickle.load(f)
        time_array_1.append(data)
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
# ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.savefig(f'multiply_time_n={n}.jpg')
# plt.show()

time_0 = time_array_1[0]
for i0 in range(len(time_array_1)):
    time_array_1[i0] = time_0/time_array_1[i0]
fig, ax = plt.subplots()
ax.set_title('np.dot()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
# ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_1, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.savefig(f'multiply_time_ratio_n={n}.jpg')
# plt.show()


time_array_2 = []
for cpu_num in cpu_num_array:
    with open(f'./task_{cpu_num}/inv_time_n={n}.pkl', 'rb') as f:
        data = pickle.load(f)
        time_array_2.append(data)
fig, ax = plt.subplots()
ax.set_title('np.linalg.inv()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
# ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_2, '-o', )
plt.savefig(f'inv_time_n={n}.jpg')
# plt.show()

time_0 = time_array_2[0]
for i0 in range(len(time_array_2)):
    time_array_2[i0] = time_0/time_array_2[i0]
fig, ax = plt.subplots()
ax.set_title('np.linalg.inv()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
# ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_2, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.savefig(f'inv_time_ratio_n={n}.jpg')
# plt.show()


time_array_3 = []
for cpu_num in cpu_num_array:
    with open(f'./task_{cpu_num}/eigen_time_n={n}.pkl', 'rb') as f:
        data = pickle.load(f)
        time_array_3.append(data)
fig, ax = plt.subplots()
ax.set_title('np.linalg.eig()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Time (s)')
# ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_3, '-o', )
plt.savefig(f'eigen_time_n={n}.jpg')
# plt.show()

time_0 = time_array_3[0]
for i0 in range(len(time_array_3)):
    time_array_3[i0] = time_0/time_array_3[i0]
fig, ax = plt.subplots()
ax.set_title('np.linalg.eig()')
ax.set_xlabel('Number of CPU cores')
ax.set_ylabel('Ratio')
# ax.xaxis.set_major_locator(MultipleLocator(1))
plt.plot(cpu_num_array, time_array_3, '-o', )
plt.plot(cpu_num_array, cpu_num_array, '--r')
plt.savefig(f'eigen_time_ratio_n={n}.jpg')
# plt.show()