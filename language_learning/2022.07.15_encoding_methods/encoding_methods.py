"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/23000
"""


string_array = ['关', '。', '3', '.']

for string in string_array:
    # 编码
    gb2312 = string.encode(encoding="gb2312")
    gbk = string.encode(encoding="gbk")
    gb18030 = string.encode(encoding="gb18030")
    uft8 = string.encode(encoding="utf-8")

    # 查看
    print('字符串 =', string, ' | 数据类型 =', type(string), ' | 长度 =', len(string))
    print('gb2312编码 =', gb2312, ' | 数据类型 =', type(gb2312), ' | 长度 =', len(gb2312))
    print('gbk编码 =', gbk, ' | 数据类型 =', type(gbk), ' | 长度 =', len(gbk))
    print('gb18030编码 =', gb18030, ' | 数据类型 =', type(gb18030), ' | 长度 =', len(gb18030))
    print('utf8编码 =', uft8, ' | 数据类型 =', type(uft8), ' | 长度 =', len(uft8))
    print()


# 乱码例子
string = '关关'
uft8 = string.encode(encoding="utf-8")
new_string_1 = uft8.decode(encoding="utf-8")
new_string_2 = uft8.decode(encoding="gbk")
print("使用utf-8解码utf-8编码的数据 =", new_string_1)
print("使用gbk解码utf-8编码的数据 =", new_string_2)