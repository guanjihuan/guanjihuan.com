"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/37672
"""

# 初始例子
import guan
response = guan.chat(prompt='你好', stream_show=1, top_p=0.8, temperature=0.8)
print('最终回答：', response, '\n')

# 一个列表排序的应用例子
import guan
import random
random_list = [random.randint(1, 100) for _ in range(5)]
print('初始随机列表：', random_list)
response = guan.chat(prompt='直接给出数组从小到大的排序结果，不需要其他说明，请保证结果是正确的：'+str(random_list), stream_show=1, top_p=0.01, temperature=0.01) # 这里把 top_p 和 temperature 降到最低可以在一定程度上保证结果的正确性。 
print('初始随机列表：', random_list)
random_list.sort()
print('算法排序后的列表：', random_list)
print('使用大语言模型排序后的列表：', response, '\n') # 效率不高，且不保证结果是百分百正确，通常对列表元素比较少的情况才有效。