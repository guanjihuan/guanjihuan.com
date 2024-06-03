"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/41201
"""

def get_break_signal_from_loss_array(loss_array, patience=10, min_delta=0.001):
    break_signal = 0
    counter = 0
    num = len(loss_array)
    for i0 in range(num):
        if i0 != 0:
            if abs(loss_array[i0]-loss_array[i0-1])<min_delta:
                counter += 1
    if counter >= patience:  # 当损失函数的变化绝对值小于 min_delta 的次数超过 patience 次后，给一个停止信号
        break_signal = 1
    print(counter)  # 查看满足条件的次数
    return break_signal

train_times = 100
for i0 in range(train_times):
    print('Training...')
    loss_array = [10, 3, 1, 0.1, 0.02, 0.003, 0.001, 0.0004, 0.0005, 0.0001, 0.0003]
    break_signal = get_break_signal_from_loss_array(loss_array, patience=4, min_delta=0.001)
    if break_signal == 1:
        break
print('Early stop:', break_signal)