"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/40353
"""

import torch
import torchviz


# 简单网络的例子
class SimpleNet(torch.nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = torch.nn.Linear(10, 6)
        self.fc2 = torch.nn.Linear(6, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
model = SimpleNet()
input = torch.randn(1, 10)
output = model(input)
graph = torchviz.make_dot(output, params=dict(model.named_parameters()))
graph.render("Simple_net_graph") # 保存计算图为 PDF 文件


# 卷积网络的例子
class ConvolutionalNeuralNetwork(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.convolutional_layer_1 = torch.nn.Conv2d(in_channels=1, out_channels=10, kernel_size=3, stride=1, padding=1)
        self.convolutional_layer_2 = torch.nn.Conv2d(in_channels=10, out_channels=10, kernel_size=3, stride=1, padding=1)
        self.pooling_layer = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.hidden_layer_1 = torch.nn.Linear(in_features=10*7*7, out_features=10)
        self.hidden_layer_2 = torch.nn.Linear(in_features=10, out_features=10)
        self.output_layer = torch.nn.Linear(in_features=10, out_features=1)
    def forward(self, x):
        channel_output_1 = torch.nn.functional.relu(self.pooling_layer(self.convolutional_layer_1(x)))
        channel_output_2 = torch.nn.functional.relu(self.pooling_layer(self.convolutional_layer_2(channel_output_1)))
        channel_output_2 = torch.flatten(channel_output_2, 1)
        hidden_output_1 = torch.nn.functional.relu(self.hidden_layer_1(channel_output_2))
        hidden_output_2 = torch.nn.functional.relu(self.hidden_layer_2(hidden_output_1))
        output = self.output_layer(hidden_output_2)
        return output
model = ConvolutionalNeuralNetwork()
input = torch.randn(15, 1, 28, 28)
output = model(input)
graph = torchviz.make_dot(output, params=dict(model.named_parameters()))
graph.render("CNN_graph") # 保存计算图为 PDF 文件