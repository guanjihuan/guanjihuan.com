"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/37680
"""

def func_example(a=1, b=2):
    for i0 in range(3):
        print(i0+1)
    c = a + b
    return a, b, c

import guan
return_data = guan.run(function_name=func_example, args=(3, 4), return_show=0, get_print=1)
print(return_data)