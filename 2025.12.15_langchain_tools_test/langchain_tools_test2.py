import guan
from langchain_core.tools import tool

@tool
def add_numbers_1(a, b):
    """将两个数字相加"""
    return str(a + b + 0.1)+'\n'

@tool
def add_numbers_2(a, b):
    """将两个数字相加"""
    return str(a + b + 0.0001)+'\n'

@tool
def subtract_numbers(a, b):
    """将两个数字相减"""
    return str(a - b)+'\n'

@tool
def guan_operator(a, b):
    """ """
    return str(a*b)+'\n'

@tool
def other_operators_1(a, b):
    """A 操作"""
    return str(a*b+0.1)+'\n'

@tool
def other_operators_2(a, b):
    """#号注释测试"""
    return str(a*b+0.2)+'\n' # B 操作

@tool
def other_operators_3(a, b):
    """变量名测试"""
    C_operation = str(a*b+0.3)+'\n'
    return C_operation

guan.langchain_chat_with_tools(prompt='计算 3+2', temperature=0.0, tools=[add_numbers_1])
print('\n\n---\n')
guan.langchain_chat_with_tools(prompt='计算 3+2。用工具里的返回结果作为最终结果。', temperature=0.0, tools=[add_numbers_1])

print('\n\n---分割线---\n')

guan.langchain_chat_with_tools(prompt='计算 3+2', temperature=0.0, tools=[add_numbers_2])
print('\n\n---\n')
guan.langchain_chat_with_tools(prompt='计算 3+2。用工具里的返回结果作为最终结果。', temperature=0.0, tools=[add_numbers_2])

print('\n\n---分割线---\n')

guan.langchain_chat_with_tools(prompt='计算 3+2', temperature=0.0, tools=[subtract_numbers])
print('\n\n---\n')
guan.langchain_chat_with_tools(prompt='计算 3+2。用工具里的返回结果作为最终结果。', temperature=0.0, tools=[subtract_numbers])

print('\n\n---分割线---\n')

all_tools = [add_numbers_1, add_numbers_2, subtract_numbers, subtract_numbers, other_operators_3, other_operators_2,  other_operators_1, guan_operator]

guan.langchain_chat_with_tools(prompt='对 3 和 2 进行 Guan 操作', temperature=0.0, tools=all_tools)
print('\n\n---\n')
guan.langchain_chat_with_tools(prompt='对 3 和 2 进行 A 操作', temperature=0.0, tools=all_tools)
print('\n\n---\n')
guan.langchain_chat_with_tools(prompt='对 3 和 2 进行 B 操作', temperature=0.0, tools=all_tools)
print('\n\n---\n')
guan.langchain_chat_with_tools(prompt='对 3 和 2 进行 C 操作', temperature=0.0, tools=all_tools)