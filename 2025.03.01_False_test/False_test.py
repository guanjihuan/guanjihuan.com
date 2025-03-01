"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45201
"""

# False 布尔值
print(bool(False))  
print(bool(0))
print(bool(0.0))
print(bool(0.0j))
print(bool(None))
print(bool('')) 
print(bool([]))
print(bool({}))
print(bool(())) 
print(bool(set()))
print()

# 虽然布尔值相同，但只有 False, 0, 0.0, 0.0j 和 False 等价
print(False==False) # True
print(False==0) # True
print(False==0.0) # True
print(False==0.0j) # True
print(False==None) # False
print(False=='') # False
print(False==[]) # False
print(False=={}) # False
print(False==()) # False
print(False==set()) # False
print()

def true_or_false(a):
    if a:
        print('True')
    else:
        print('False')

# 'if' 环境中的 False 测试
true_or_false(False)
true_or_false(0)
true_or_false(0.0)
true_or_false(0.0j)
true_or_false(None)
true_or_false('')
true_or_false([])
true_or_false({})
true_or_false(())
true_or_false(set())
print()

# 'if' 环境中的 True 测试
true_or_false(True)
true_or_false('True')
true_or_false('False')
true_or_false('a')
true_or_false(1)
true_or_false(-1)
true_or_false(2)
print()