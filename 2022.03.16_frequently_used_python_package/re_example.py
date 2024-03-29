import re

# 正则表达式：匹配任意字符（.）；零次或多次（*）；尽可能少地匹配（?）

# re.match 指匹配起始位置的模式，如果起始位置不匹配的话，返回 None
string = 'this_is_a_test_abc_123'
result = re.match(pattern='ab(.*?)23', string=string)
print(result)
print()
result = re.match(pattern='this(.*?)abc', string=string)
print(result.group(0))
print(result.group(1))
print()

# re.search 扫描整个字符串并返回第一个成功的匹配。
string = 'this_is_a_test_abc_123'
result = re.search(pattern='ab(.*?)23', string=string)
print(result.group(0))
print(result.group(1))
print()
result = re.search(pattern='this(.*?)abc', string=string)
print(result.group(0))
print(result.group(1))