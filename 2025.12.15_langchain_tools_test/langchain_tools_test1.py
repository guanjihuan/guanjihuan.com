import guan
from langchain_core.tools import tool

@tool
def add_numbers_1(a, b):
    """将两个数字相加"""
    return str(a + b + 1)+'\n'

guan.langchain_chat_with_tools(prompt='计算 3+2', model="qwen-max", temperature=0.0, tools=[add_numbers_1])
print('\n\n---\n')
guan.langchain_chat_with_tools(prompt='计算 3+2。强制使用工具里的返回结果作为最终结果。', model="qwen-max", temperature=0.0, tools=[add_numbers_1])