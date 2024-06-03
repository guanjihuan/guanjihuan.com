from torch.utils.data import DataLoader, TensorDataset
import torch
for i0 in range(5):
    x_train = torch.randn(100, 20) # 小文件加载
    y_train = torch.randn(100, 1) # 小文件加载
    train_dataset = TensorDataset(x_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    for batch_x, batch_y in train_loader:
        print(batch_x.shape)
        print(batch_y.shape)
    if i0 == 0:
        print('Training model...')
    else:
        print('Continue training model...')