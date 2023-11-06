"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/154
"""

# import tensorflow as tf
import tensorflow.compat.v1 as tf  # 之所以这么调用，是因为tensorflow版本2.0无法兼容版本1.0
tf.compat.v1.disable_eager_execution()  # 这行代码可以保证 sess.run() 能够正常运行
import numpy as np
import matplotlib.pyplot as plt


def add_layer(inputs, in_size, out_size, activation_function=None):  # 定义一层的所有神经元
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))  # 定义Weights为tf变量，并给予初值
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)  # 定义biases为tf变量，并给予初值
    Wx_plus_b = tf.matmul(inputs, Weights) + biases  # 得分
    if activation_function is None:  # 没有激活函数
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)  # 使用激活函数
    return outputs  # 返回该层每个神经元的输出值（维度为out_size）


# 产生训练的数据
x_data = np.linspace(-1, 1, 300, dtype=np.float32)[:, np.newaxis]  # 产生数据，作为神经网络的输入数据。注：[:, np.newaxis]是用来增加一个轴，变成一个矩阵。
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)  # 产生噪声
y_data = np.square(x_data) - 0.5 + noise  # x_data加上噪声，作为神经网络的输出数据。
print(x_data.shape)  # 查看数据维度
print(noise.shape)  # 查看数据维度
print(y_data.shape)  # 查看数据维度
print()  # 打印输出空一行


# 神经网络模型的建立
xs = tf.placeholder(tf.float32, [None, 1])  # 定义占位符，为神经网络训练的输入数据。这里的None代表无论输入有多少数据都可以
ys = tf.placeholder(tf.float32, [None, 1])  # 定义占位符，为神经网络训练的输出数据。
l1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)  # 增加一个隐藏层
prediction = add_layer(l1, 10, 1, activation_function=None)  # 输出层
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))  # 损失函数
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)  # 梯度下降
init = tf.global_variables_initializer()  # 变量初始化

# 画出原始的输入输出数据点图
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(x_data, y_data)
plt.ion()  # 开启交互模式
plt.show()  # 显示图像

# 训练神经网络模型
sess = tf.Session()  # 启动一个会话
sess.run(init)  # 初始化变量
for i in range(1000):  # 训练1000次
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})  # 喂数据，梯度下降循环1000次。
    if i % 50 == 0:  # 每训练50次画一下图
        try:  # to visualize the result and improvement
            ax.lines.remove(lines[0])
        except Exception:
            pass
        prediction_value = sess.run(prediction, feed_dict={xs: x_data})  # 神经网络预测的值
        print('loss=', sess.run(loss, feed_dict={xs: x_data, ys: y_data}))  # 打印输出，查看损失函数下降情况
        print('prediction=', sess.run(prediction, feed_dict={xs: [x_data[0, :]]}))  # # 打印输出神经网络预测的值
        print()  # 打印空一行
        lines = ax.plot(x_data, prediction_value, 'r-', lw=5) # 画出预测的值，用线连起来
        plt.pause(.1)  # 暂停0.1，防止画图过快看不清。
plt.ioff()  # 关闭交互模式，再画一次图。作用是不让图自动关掉。
lines = ax.plot(x_data, prediction_value, 'r-', lw=5)
plt.show()


# 保存训练好的神经网络模型tf.train.Saver()
saver = tf.train.Saver()
save_path = saver.save(sess, "./my_net/save_net.ckpt")  # 保存模型
print("Save to path: ", save_path)
print()
sess.close()  # 关闭会话


# 调用神经网络模型，来预测新的值
with tf.Session() as sess2:
    saver.restore(sess2, "./my_net/save_net.ckpt")  # 提取模型中的所有变量
    print(y_data[0, :])  # 输出的原始值
    print(sess2.run(prediction, feed_dict={xs: [x_data[0, :]]}))  # 预测值

