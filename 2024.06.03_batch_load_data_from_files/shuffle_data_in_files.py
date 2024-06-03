import torch

def load_data_from_file(filename):
    x_train = torch.randn(100, 20) # 小文件加载
    y_train = torch.randn(100, 1) # 小文件加载
    return x_train, y_train

x_train_new = []  # 新的小文件
y_train_new = []  # 新的小文件
n = 5
for i0_new in range(n):
    for i0 in range(n):
        x_train, y_train = load_data_from_file(filename=str(i0))
        if i0 == 0:
            x_train_new = x_train[i0_new*int(100/n):(i0_new+1)*int(100/n), :]
            y_train_new = y_train[i0_new*int(100/n):(i0_new+1)*int(100/n), :]
        else:
            x_train_new = torch.cat((x_train_new, x_train[i0_new*int(100/n):(i0_new+1)*int(100/n), :]), dim=0)
            y_train_new = torch.cat((y_train_new, y_train[i0_new*int(100/n):(i0_new+1)*int(100/n), :]), dim=0)
    print(x_train_new.shape)
    print(y_train_new.shape)
    print('Save new file!')