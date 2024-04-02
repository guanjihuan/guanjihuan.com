import torch
input_data = torch.tensor([[7, 3, 5, 2],
                           [8, 7, 1, 6],
                           [4, 9, 3, 9],
                           [0, 8, 4, 5]], dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # 两次 .unsqueeze(0) 分别是添加批次和通道维度

max_pool = torch.nn.MaxPool2d(kernel_size=2, stride=2)
output_data = max_pool(input_data)

print("Input:\n", input_data)
print("Output after max pooling:\n",  output_data)
print('输入数据的形状: ', input_data.shape)
print('输出数据的形状: ', output_data.shape)