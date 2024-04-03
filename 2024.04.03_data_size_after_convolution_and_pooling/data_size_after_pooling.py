"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/39320
"""

import torch
input_data = torch.randn(1, 1, 28, 28)

print('【不同卷积核大小对输出数据的维度的影响】')
max_pool = torch.nn.MaxPool2d(kernel_size=1, stride=1)
output_data = max_pool(input_data)
print("维度（卷积核大小为1）：", output_data.shape)
max_pool = torch.nn.MaxPool2d(kernel_size=2, stride=1)
output_data = max_pool(input_data)
print("维度（卷积核大小为2）：", output_data.shape)
max_pool = torch.nn.MaxPool2d(kernel_size=3, stride=1)
output_data = max_pool(input_data)
print("维度（卷积核大小为3）：", output_data.shape)

print()
print('【不同步幅对输出数据的维度的影响（以卷积核大小为2为例）】')
max_pool = torch.nn.MaxPool2d(kernel_size=2, stride=1)
output_data = max_pool(input_data)
print("维度（步幅为1）：", output_data.shape)
max_pool = torch.nn.MaxPool2d(kernel_size=2, stride=2)
output_data = max_pool(input_data)
print("维度（步幅为2）：", output_data.shape)
max_pool = torch.nn.MaxPool2d(kernel_size=2, stride=3)
output_data = max_pool(input_data)
print("维度（步幅为3）：", output_data.shape)