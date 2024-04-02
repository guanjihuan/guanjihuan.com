import torch
input_data = torch.randn(1, 1, 28, 28)

conv_layer = torch.nn.Conv2d(in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=1)
output_data = conv_layer(input_data)
print("输出数据的形状：", output_data.shape)

conv_layer = torch.nn.Conv2d(in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=0)
output_data = conv_layer(input_data)
print("输出数据的形状：", output_data.shape)