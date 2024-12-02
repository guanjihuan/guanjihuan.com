"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/43720
"""

from torchvision import datasets, transforms

transform = transforms.Compose([transforms.ToTensor()]) # 定义数据预处理步骤（转换为Tensor）
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform) # 加载 MNIST 数据集，训练集
print(type(train_dataset))
size_of_train_dataset = len(train_dataset)
print(size_of_train_dataset)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform) # 加载 MNIST 数据集，测试集
print(type(test_dataset))
size_of_test_dataset = len(test_dataset)
print(size_of_test_dataset)

import random
rand_number = random.randint(0, size_of_train_dataset-1)
image, label = train_dataset[rand_number] # 获取一张图像和标签
print(type(image))
print(image.shape)
image = image.squeeze(0)  # 去掉单通道的维度 (1, 28, 28) -> (28, 28)
print(type(image))
print(image.shape)

import matplotlib.pyplot as plt
# import os
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE" # 解决可能的多个 OpenMP 库版本冲突的问题。如果有 OMP 报错，可以试着使用这个解决。
plt.imshow(image, cmap='gray') # 显示图像
plt.title(f"Label: {label}")  # 标签值（理论值）
plt.axis('off')  # 不显示坐标轴
plt.show()