"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/41194
"""

import torch

# 定义两个张量
tensor1 = torch.randn(2, 3)
tensor2 = torch.randn(2, 3)
print(tensor1)
print(tensor2)
print()

# 第一维度的数据合并（需要其他的维度保持一致）
result1 = torch.cat((tensor1, tensor2), dim=0)
print(result1)
print(result1.shape)
print()

# 第二维度的数据合并（需要其他的维度保持一致）
result2 = torch.cat((tensor1, tensor2), dim=1)
print(result2)
print(result2.shape)
print()



# 定义多个张量
tensor1 = torch.randn(2, 10)
tensor2 = torch.randn(2, 20)
tensor3 = torch.randn(2, 30)
tensor4 = torch.randn(2, 50)

# 将这些张量放在一个列表中
tensors = [tensor1, tensor2, tensor3, tensor4]

# 第二维度的数据合并（确保所有张量的第一维度相同）
result3 = torch.cat(tensors, dim=1)
print(result3.shape)