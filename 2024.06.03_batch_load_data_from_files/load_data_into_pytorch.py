from torch.utils.data import DataLoader, TensorDataset
import torch
x_train = torch.randn(500, 20) # 全部数据加载
y_train = torch.randn(500, 1) # 全部数据加载
train_dataset = TensorDataset(x_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
for batch_x, batch_y in train_loader:
    print(batch_x.shape)
    print(batch_y.shape)