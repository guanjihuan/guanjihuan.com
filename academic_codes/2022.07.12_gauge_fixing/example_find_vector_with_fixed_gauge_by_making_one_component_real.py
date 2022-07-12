"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/22604
"""


import numpy as np
import cmath

def find_vector_with_fixed_gauge_by_making_one_component_real(vector, precision=0.005, index=None):
    vector = np.array(vector)
    if index == None:
        index = np.argmax(np.abs(vector))
    sign_pre = np.sign(np.imag(vector[index]))
    for phase in np.arange(0, 2*np.pi, precision):
        sign =  np.sign(np.imag(vector[index]*cmath.exp(1j*phase)))
        if np.abs(np.imag(vector[index]*cmath.exp(1j*phase))) < 1e-9 or sign == -sign_pre:
            break
        sign_pre = sign
    vector = vector*cmath.exp(1j*phase)
    if np.real(vector[index]) < 0:
        vector = -vector
    return vector 

vector_1 = np.array([np.sqrt(0.5), np.sqrt(0.5)])*cmath.exp(np.random.uniform(0, 1)*1j)
vector_2 = np.array([1, 0])*cmath.exp(np.random.uniform(0, 1)*1j)

print('\n随机规范的原向量：', vector_1)
vector_1 = find_vector_with_fixed_gauge_by_making_one_component_real(vector_1, precision=0.001)
print('固定规范后的向量：', vector_1)

print('\n随机规范的原向量：', vector_2)
vector_2 = find_vector_with_fixed_gauge_by_making_one_component_real(vector_2, precision=0.001)
print('固定规范后的向量：', vector_2)


# # 可直接使用Guan软件包来调用以上函数：https://py.guanjihuan.com。
# # 安装命令：pip install --upgrade guan。

# import guan

# print('\n随机规范的原向量：', vector_1)
# vector_1 = guan.find_vector_with_fixed_gauge_by_making_one_component_real(vector_1, precision=0.001)
# print('固定规范后的向量：', vector_1)

# print('\n随机规范的原向量：', vector_2)
# vector_2 = guan.find_vector_with_fixed_gauge_by_making_one_component_real(vector_2, precision=0.001)
# print('固定规范后的向量：', vector_2)