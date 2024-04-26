"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/124
"""

# import tensorflow as tf  # 导入tensorflow

import tensorflow.compat.v1 as tf  # 之所以这么调用，是因为tensorflow版本2.0无法兼容版本1.0
tf.compat.v1.disable_eager_execution()  # 这行代码可以保证 sess.run() 能够正常运行
# tf.disable_v2_behavior() # 或者使用这个代码，可代替上面一行

greeting = tf.constant('Hello Google Tensorflow!')  # 定义一个常量

# 第一种方式
sess = tf.Session()  # 启动一个会话
result = sess.run(greeting)  # 使用会话执行greeting计算模块
print(result)  # 打印显示
sess.close()  # 关闭会话

# 第二种方式
with tf.Session() as sess:  # 启动一个会话
    print(sess.run(greeting))  # 打印显示


# 例子1：
matrix1 = tf.constant([[1., 3.]])  # 定义常数矩阵1  tf.constant()
matrix2 = tf.constant([[2.], [2.]])  # 定义常数矩阵2  tf.constant()
product = tf.matmul(matrix1, matrix2)  # 矩阵乘积  tf.matmul()
linear = tf.add(product, tf.constant(2.))  # 矩阵乘积后再加上一个常数  tf.add()
with tf.Session() as sess:  # 启动一个会话  tf.Session()
    print(sess.run(matrix1))  # 执行语句并打印显示  tf.Session().run
    print(sess.run(linear))  # 执行语句并打印显示  tf.Session().run
print(linear)  # 直接打印是不能看到计算结果的，因为还未执行，只是一个张量。这里打印显示的结果是：Tensor("Add:0", shape=(1, 1), dtype=float32)


# 例子2：变量tf.Variable()
state = tf.Variable(3, name='counter')  # 变量tf.Variable
init = tf.global_variables_initializer()  # 如果定义了变量,后面一定要有这个语句，用来初始化变量。
with tf.Session() as sess:
    sess.run(init)  # 初始化变量
    print(sess.run(state))  # 执行语句并打印显示

# 例子3：占位符tf.placeholder()，用来临时占坑，需要用feed_dict来传入数值。
x1 = tf.placeholder(tf.float32)
x2 = tf.placeholder(tf.float32)
y = x1 + x2
with tf.Session() as sess:
    print(sess.run(y, feed_dict={x1: 7, x2: 2}))