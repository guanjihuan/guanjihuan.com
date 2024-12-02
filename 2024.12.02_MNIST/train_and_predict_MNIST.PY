"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/43720
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import datasets, transforms

transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,), (0.5,))])  # 数据转换（将图片转换为 Tensor 并进行归一化处理，均值和标准差为 0.5）
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform) # 下载训练数据集
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform) # 下载测试数据集

# 训练函数
def train(model, train_loader, criterion, optimizer, num_epochs=5):
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for images, labels in train_loader:
            # print(images.shape)
            optimizer.zero_grad()  # 清除以前的梯度
            outputs = model(images) # 前向传播
            loss = criterion(outputs, labels)
            loss.backward() # 反向传播和优化
            optimizer.step()  
            running_loss += loss.item() 
            _, predicted = torch.max(outputs, 1) # 计算准确率
            total += labels.size(0)
            correct += (predicted == labels).sum().item()     
        avg_loss = running_loss / len(train_loader)
        accuracy = 100 * correct / total
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%')

# 测试函数
def test(model, test_loader):
    model.eval()  # 设置为评估模式
    correct = 0
    total = 0
    with torch.no_grad():  # 禁用梯度计算
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    print(f'Test Accuracy: {accuracy:.2f}%')

# 训练和测试
def train_and_test(model, train_loader, test_loader):
    criterion = nn.CrossEntropyLoss()  # 交叉熵损失
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    train(model, train_loader, criterion, optimizer, num_epochs=10)
    test(model, test_loader)

# 扁平化数据，并重建 DataLoader（用于全连接神经网络输入端的数据处理）
def flatten_data(data_loader): 
    images_array = []
    labels_array = []
    for images, labels in data_loader:
        images = torch.flatten(images, start_dim=1) # 除去batch维度后，其他维度展平
        images_array.append(images)
        labels_array.append(labels)
    images_array = torch.cat(images_array, dim=0)
    labels_array = torch.cat(labels_array, dim=0)
    dataset_new = TensorDataset(images_array, labels_array)
    loader_new = DataLoader(dataset_new, batch_size=64, shuffle=True)
    return loader_new

# 数据加载器
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 扁平化数据
train_loader_new = flatten_data(train_loader)
test_loader_new = flatten_data(test_loader)

# 安装软件包：pip install --upgrade guan
import guan

hidden_size = 64

print('---全连接神经网络模型（包含一个隐藏层）---')
model = guan.fully_connected_neural_network_with_one_hidden_layer(input_size=28*28, hidden_size=hidden_size, output_size=10, activation='relu')
train_and_test(model, train_loader_new, test_loader_new)

print('---全连接神经网络模型（包含两个隐藏层）---')
model = guan.fully_connected_neural_network_with_two_hidden_layers(input_size=28*28, hidden_size_1=hidden_size, hidden_size_2=hidden_size, output_size=10, activation_1='relu', activation_2='relu')
train_and_test(model, train_loader_new, test_loader_new)

print('---全连接神经网络模型（包含三个隐藏层）---')
model = guan.fully_connected_neural_network_with_three_hidden_layers(input_size=28*28, hidden_size_1=hidden_size, hidden_size_2=hidden_size, hidden_size_3=hidden_size, output_size=10, activation_1='relu', activation_2='relu', activation_3='relu')
train_and_test(model, train_loader_new, test_loader_new)

print('---卷积神经网络模型（包含两个卷积层和两个全连接层）---')
model = guan.convolutional_neural_network_with_two_convolutional_layers_and_two_fully_connected_layers(in_channels=1, out_channels_1=32, out_channels_2=64, kernel_size_1=3, kernel_size_2=3, stride_1=1, stride_2=1, padding_1=1, padding_2=1, pooling=1, pooling_kernel_size=2, pooling_stride=2, input_size=7*7*64, hidden_size_1=hidden_size, hidden_size_2=hidden_size, output_size=10)
train_and_test(model, train_loader, test_loader)