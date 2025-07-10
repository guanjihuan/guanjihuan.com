import guan

@guan.try_decorator
def test1(a, b):
    print(a)
    bug_code
    print(b)
    return 'return_message1'
    
result1 = test1(10, b=20)
print(result1)

print()

def test2(a, b):
    print(a)
    bug_code
    print(b)
    return 'return_message2'

result2 = guan.try_except(test2, 100, b=200)
print(result2)