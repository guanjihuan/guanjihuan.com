import guan

def test1(a, b):
    print(a)
    bug_code
    print(b)
    return 'return_message1'

result1 = guan.try_except(test1, 10, b=20)
print(result1)

print()

@guan.try_decorator
def test2(a, b):
    print(a)
    bug_code
    print(b)
    return 'return_message2'
    
result2 = test2(100, b=200)
print(result2)