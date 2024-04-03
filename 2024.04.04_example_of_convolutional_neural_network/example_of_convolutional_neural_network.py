"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/39368
"""

def convolutional_neural_network_with_two_convolutional_layers_and_two_fully_connected_layers(in_channels=1, out_channels_1=10, out_channels_2=10, kernel_size_1=3, kernel_size_2=3, stride_1=1, stride_2=1, padding_1=0, padding_2=0, pooling=1, pooling_kernel_size=2, pooling_stride=2, input_size=1, hidden_size_1=10, hidden_size_2=10, output_size=1):
    import torch
    global model_class_of_convolutional_neural_network_with_two_convolutional_layers_and_two_fully_connected_layers
    class model_class_of_convolutional_neural_network_with_two_convolutional_layers_and_two_fully_connected_layers(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.convolutional_layer_1 = torch.nn.Conv2d(in_channels=in_channels, out_channels=out_channels_1, kernel_size=kernel_size_1, stride=stride_1, padding=padding_1)
            self.convolutional_layer_2 = torch.nn.Conv2d(in_channels=out_channels_1, out_channels=out_channels_2, kernel_size=kernel_size_2, stride=stride_2, padding=padding_2)
            self.pooling_layer = torch.nn.MaxPool2d(kernel_size=pooling_kernel_size, stride=pooling_stride)
            self.hidden_layer_1 = torch.nn.Linear(input_size, hidden_size_1)
            self.hidden_layer_2 = torch.nn.Linear(hidden_size_1, hidden_size_2)
            self.output_layer = torch.nn.Linear(hidden_size_2, output_size)
        def forward(self, x):
            if pooling == 1:
                channel_output_1 = torch.nn.functional.relu(self.pooling_layer(self.convolutional_layer_1(x)))
                print('第一个卷积和池化后的维度：', channel_output_1.shape)
                channel_output_2 = torch.nn.functional.relu(self.pooling_layer(self.convolutional_layer_2(channel_output_1)))
                print('第二个卷积和池化后的维度：', channel_output_1.shape)
            else:
                channel_output_1 = torch.nn.functional.relu(self.convolutional_layer_1(x))
                print('第一个卷积后的维度：', channel_output_1.shape)
                channel_output_2 = torch.nn.functional.relu(self.convolutional_layer_2(channel_output_1))
                print('第二个卷积后的维度：', channel_output_1.shape)
            channel_output_2 = torch.flatten(channel_output_2, 1)
            print('扁平后的维度：', channel_output_2.shape)
            hidden_output_1 = torch.nn.functional.relu(self.hidden_layer_1(channel_output_2))
            print('第一个全连接层后的维度：', hidden_output_1.shape)
            hidden_output_2 = torch.nn.functional.relu(self.hidden_layer_2(hidden_output_1))
            print('第二个全连接层后的维度：', hidden_output_1.shape)
            output = self.output_layer(hidden_output_2)
            print('输出数据的维度：', output.shape)
            return output
    model = model_class_of_convolutional_neural_network_with_two_convolutional_layers_and_two_fully_connected_layers()
    return model


import torch
input = torch.randn(15, 1, 28, 28)

print('【卷积和池化过程的维度变化】')
model = convolutional_neural_network_with_two_convolutional_layers_and_two_fully_connected_layers(in_channels=1, out_channels_1=10, out_channels_2=10, kernel_size_1=3, kernel_size_2=3, stride_1=1, stride_2=1, padding_1=1, padding_2=1, pooling=1, pooling_kernel_size=2, pooling_stride=2, input_size=10*7*7, hidden_size_1=10, hidden_size_2=10, output_size=1)
output = model(input)
print()

print('【卷积过程的维度变化（无池化）】')
model = convolutional_neural_network_with_two_convolutional_layers_and_two_fully_connected_layers(in_channels=1, out_channels_1=10, out_channels_2=10, kernel_size_1=3, kernel_size_2=3, stride_1=1, stride_2=1, padding_1=1, padding_2=1, pooling=0, pooling_kernel_size=2, pooling_stride=2, input_size=10*28*28, hidden_size_1=10, hidden_size_2=10, output_size=1)
output = model(input)