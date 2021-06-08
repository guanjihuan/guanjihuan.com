"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6846
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re  # 正则模块
import requests
import os
# os.chdir('D:')  # 设置文件保存的位置


# 输入
address_array = []
for i in range(10):  # 最多一次性下载10篇
    address = input('\n输入DOI/链接/标题：')
    address_array.append(address)
    continue_or_not = input('\n继续添加（1）/不继续添加（0）：')
    if int(continue_or_not) == 0:
        break

# 下载
for address in address_array:
    r = requests.post('https://sci-hub.st/', data={'request': address})
    print('\n响应结果是：', r)
    print('访问的地址是：', r.url)
    soup = BeautifulSoup(r.text, features='lxml')
    pdf_URL = soup.iframe['src']
    if re.search(re.compile('^https:'), pdf_URL):
        pass
    else:
        pdf_URL = 'https:'+pdf_URL
    print('PDF的地址是：', pdf_URL)
    name = re.search(re.compile('fdp.*?/'),pdf_URL[::-1]).group()[::-1][1::]
    print('PDF文件名是：', name)
    print('保存的位置在：', os.getcwd())
    print('\n正在下载')
    r = requests.get(pdf_URL, stream=True)
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)
    print('下载完成！')

print('\n全部下载完成！')