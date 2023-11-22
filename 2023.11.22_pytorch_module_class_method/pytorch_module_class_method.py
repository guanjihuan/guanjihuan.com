"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/37753
"""

import torch

# 第一部分：torch.nn.Linear，线性变换层。公式为：y = x A^T + b

linear_layer = torch.nn.Linear(20, 3)  # (in_size, out_size)，其中权重（weight）和偏置（bias）默认是从均匀分布（uniform distribution）中进行初始化的。
input = torch.randn(128, 20) # 128个样本
output = linear_layer(input) # 获取线性层的输出数据
print(input.size())
print(output.size())
print()



# 第二部分：torch.nn.ReLU，修正线性单元（Rectified Linear Unit，ReLU）激活函数 。公式为：y = max(0,x)

relu_layer = torch.nn.ReLU()
x = torch.tensor([-1.0, 2.0, -3.0])
y = relu_layer(x)
print(y)
print()



# 第三部分：torch.nn.MSELoss，均方误差损失（Mean Squared Error Loss），也被称为 L2 损失。公式为：MSE Loss = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2

target = torch.tensor([3.0, 4.0, 5.0], requires_grad=True) # 目标值。requires_grad 被设置为True，PyTorch会自动追踪对该张量的操作，并构建一个计算图，以便在反向传播过程中计算梯度。
predictions = torch.tensor([2.9, 4.1, 5.3], requires_grad=True) # 预测值
criterion = torch.nn.MSELoss() # 创建 MSELoss 对象
loss = criterion(predictions, target) # 计算均方误差
print('MSE Loss:', loss.item()) # 打印损失值
loss.backward()  #  反向传播。loss.backward() 仅仅负责计算梯度，不负责模型参数的更新。
# 补充说明：反向传播通过求导的链式法则进行计算。如果没有链式法则，计算梯度需要重新进行每个参数的正向传播，这就意味着每个参数的梯度计算都要单独进行一次前向传播，计算量会特别大。
print('Gradients w.r.t. target:', target.grad) # 查看目标值的梯度
print('Gradients w.r.t. predictions:', predictions.grad) # 查看预测值的梯度
print()




# 第四部分：以下为一个神经网络的例子。其中，torch.optim.SGD为优化器，用于实现随机梯度下降（Stochastic Gradient Descent，SGD）

import torch
import matplotlib.pyplot as plt

class LinearRegressionModel(torch.nn.Module):  # 定义模型，继承torch.nn.Module类
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()  # 调用父类的的初始化内容
        self.hidden_layer = torch.nn.Linear(input_size, hidden_size) # 定义一个隐藏层
        self.output_layer = torch.nn.Linear(hidden_size, output_size) # 定义一个输出层
        self.relu_layer = torch.nn.ReLU()  

    def forward(self, x):
        hidden_output = self.relu_layer(self.hidden_layer(x)) # 第一个隐藏层的输出，并使用ReLU激活函数
        # hidden_output = torch.nn.functional.relu(self.hidden_layer(x)) # 激活函数也可以用torch.nn.functional.relu()
        output = self.output_layer(hidden_output) # 输出层的输出
        return output

# 训练的数据
import numpy as np
x_data = np.linspace(-1, 1, 300, dtype=np.float32)[:, np.newaxis]  # 产生数据，作为神经网络的输入数据。注：[:, np.newaxis]是用来增加一个轴，变成一个矩阵。
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)  # 产生噪声
y_data = np.square(x_data) - 0.5 + noise  # x_data加上噪声，作为神经网络的输出数据。
print(x_data.shape)
print(noise.shape)
print(y_data.shape)
x_data = torch.from_numpy(x_data) # 转换成tensor
y_data = torch.from_numpy(y_data) # 转换成tensor
print(x_data.shape)
print(x_data.shape)
print(x_data.size())
print(x_data.size())

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(x_data, y_data)
plt.ion()  # 开启交互模式
plt.show()  # 显示图像

# 创建模型，定义损失函数和优化器
input_size = 1
hidden_size = 50
output_size = 1
model = LinearRegressionModel(input_size, hidden_size, output_size)  # 创建模型
criterion = torch.nn.MSELoss()  # 定义损失函数
learning_rate = 0.01  # 梯度下降的学习速率
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)  # 定义优化器。其中.parameters()是torch.nn.Module类中的方法

# 训练模型
num_epochs = 3000 # 迭代次数
losses = []  # 用于收集损失值
for epoch in range(num_epochs):  # 开始训练
    outputs = model.forward(x_data) # 前向传播。由于继承了torch.nn.Module类，默认使用forward方法，因此这里无需显式写出forward方法
    loss = criterion(outputs, y_data)  # 计算损失值
    optimizer.zero_grad() # 在每次训练的迭代，梯度清零
    loss.backward()  # 反向传播，计算梯度
    optimizer.step() # 更新参数
    losses.append(loss.item()) # 记录损失值
    if (epoch + 1) % 50 == 0:  # 迭代一定周期后显示一次
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass
        with torch.no_grad(): # 在推断或预测时，这个可以防止PyTorch 记录梯度信息，从而减小内存占用。这里不用也可以。
            predictions = model(x_data) # 当前迭代模型的预测结果
            lines = ax.plot(x_data.detach().numpy(), predictions.detach().numpy(), 'ro-', lw=3) # 画出预测的值，用线连起来。其中，.detach() 是 PyTorch 中的一个方法，它用于创建一个新的张量，该张量与原始张量共享相同的数据，但不再具有梯度计算的历史。
        plt.pause(.1)  # 暂停0.1秒

plt.ioff()
lines = ax.plot(x_data.detach().numpy(), predictions.detach().numpy(), 'ro-', lw=3)
plt.show()

plt.plot(losses, 'o-', label='Loss') # 绘制训练过程中的损失曲线
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

torch.save(model.state_dict(), 'model.pth')  # 使用 torch.save 函数来保存模型。其中，model.state_dict()返回模型的权重字典
torch.save(model, 'full_model.pth') # 保存整个模型，包括模型的结构和权重

model_2 = LinearRegressionModel(input_size, hidden_size, output_size)  # 创建模型
model_2.load_state_dict(torch.load('model.pth')) # 加载模型参数
with torch.no_grad(): 
    predictions_2 = model_2(x_data)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x_data, y_data)
    lines = ax.plot(x_data.detach().numpy(), predictions_2.detach().numpy(), 'bo-', lw=3)
    plt.show()

model_3 = torch.load('full_model.pth')  # 加载完整模型
with torch.no_grad(): 
    predictions_3 = model_3(x_data)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x_data, y_data)
    lines = ax.plot(x_data.detach().numpy(), predictions_3.detach().numpy(), 'go-', lw=3)
    plt.show()