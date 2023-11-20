"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/37468
"""

import torch
import numpy as np

# Torch数据类型【和NumPy相近，但不是同一个类型】

scalar = torch.tensor(3.14) # 创建一个Torch标量
print('\nTorch标量：\n', scalar)

vector = torch.tensor([1, 2, 3]) # 创建一个Torch向量
print('\n\nTorch向量：\n', vector)

matrix = torch.tensor([[1, 2, 3], [4, 5, 6]]) # # 创建一个Torch矩阵
print('\n\nTorch矩阵：\n', matrix)

int_tensor = torch.IntTensor([2])
float_tensor = torch.FloatTensor([2])
double_tensor = torch.DoubleTensor([2])
print('\n\n')
print(int_tensor)
print(float_tensor)
print(double_tensor)
print('张量在 CPU 或 GPU ：', int_tensor.device)


# Torch数据和NumPy数据的转换

numpy_array = np.arange(6).reshape((2, 3))  # NumPy数组
torch_tensor = torch.from_numpy(numpy_array)  # NumPy数组转Torch张量
numpy_array_2 = torch_tensor.numpy()  # Torch张量转NumPy数组
print('\n\n\n\nNumPy数组：\n', numpy_array)
print('\n\nNumpy数组转Torch张量：\n', torch_tensor) 
print('\n\nTorch张量转NumPy数组：\n', numpy_array_2)



# torch.from_numpy() 和 torch.tensor() 的关系【前者共享内存，后者不共享内存】
print('\n\n\n\ntorch.from_numpy() 和 torch.tensor() 的关系：')

np_array = np.array([1, 2, 3])
torch_tensor = torch.from_numpy(np_array)  # 共享内存
torch_tensor[0] = 100  # 修改Torch张量
print(np_array)  # NumPy数组也会被修改
np_array[1] = 200  # 修改NumPy数组
print(torch_tensor)  # Torch张量也会被修改

print()
np_array_2 = np.array([1, 2, 3])
torch_tensor_2 = torch.tensor(np_array_2)  # 不共享内存
torch_tensor_2[0] = 100  # 修改Torch张量
print(np_array_2)  # NumPy数组不会被修改
np_array_2[1] = 200   # 修改NumPy数组
print(torch_tensor_2)  # Torch张量不会被修改




# .numpy() 和 np.array() 的关系【前者共享内存，后者不共享内存】
print('\n\n\n\n.numpy() 和 np.array() 的关系：')

torch_tensor = torch.tensor([1, 2, 3])
numpy_array = torch_tensor.numpy()  # 共享内存
numpy_array[0] = 100  # 修改NumPy数组
print(torch_tensor)  # Torch张量会被修改
torch_tensor[1] = 200  # 修改Torch张量
print(numpy_array)   # NumPy数组也会被修改

print()
torch_tensor_2 = torch.tensor([1, 2, 3])
numpy_array_2 = np.array(torch_tensor_2)  # 不共享内存
numpy_array_2[0] = 100  # 修改NumPy数组
print(torch_tensor_2)  # Torch张量不会被修改
torch_tensor_2[1] = 200 # 修改Torch张量
print(numpy_array_2)   # NumPy数组不会被修改




# 绝对值操作

print('\n\n\n\nNumPy绝对值和Torch绝对值：')
numpy_array = [-1, -2, 1, 2]
torch_tensor = torch.tensor(numpy_array)
float_tensor = torch.FloatTensor(numpy_array)  # Torch的浮点张量
print(np.abs(numpy_array))
print(np.abs(torch_tensor))  # 不报错。numpy.abs()也可以处理tensor数据，仍然是返回Torch张量
print(np.abs(float_tensor))  # 不报错。numpy.abs()也可以处理tensor数据，仍然是返回Torch张量
print()
# print(torch.abs(numpy_array))  # 报错。torch.abs()只能处理tensor数据
print(torch.abs(torch_tensor))
print(torch.abs(float_tensor))





# 矩阵乘积操作

A = torch.tensor([[1, 2], [3, 4]])
B = torch.tensor([[5, 6], [7, 8]])
result_mm = torch.mm(A, B) # 使用torch.mm执行矩阵乘积
result_matmul = torch.matmul(A, B) # 使用torch.matmul执行矩阵乘积
print("\n\n\n\n使用torch.mm()：\n", result_mm)
print("\n使用torch.matmul()：\n", result_matmul)

result_np_dot = np.dot(A, B) # np.dot()也可以处理tensor数据，但这里返回的是NumPy数组格式
print('\n', type(result_np_dot))
print(result_np_dot, '\n')

# A_array = np.array([[1, 2], [3, 4]])
# B_array = np.array([[5, 6], [7, 8]])
# result_mm = torch.mm(A_array, B_array) # 报错。torch.mm只能处理tensor数据
# result_matmul = torch.matmul(A_array, B_array) #报错。torch.matmul只能处理tensor数据