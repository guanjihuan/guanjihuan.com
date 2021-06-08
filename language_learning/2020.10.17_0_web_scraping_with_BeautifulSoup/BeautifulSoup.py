from bs4 import BeautifulSoup
from urllib.request import urlopen

# 最简单的情况
html = urlopen("https://mofanpy.com/static/scraping/basic-structure.html").read().decode('utf-8')
print('\n显示网页的代码信息1：\n\n ----------------开始----------------\n', html, '\n\n----------------结束----------------')  # 显示网页的代码信息

soup = BeautifulSoup(html, features='lxml')   # 把网页放进BeautifulSoup
print('\n获取标签_标题h1_中的内容soup.h1：\n', soup.h1)
print('\n获取标签_段落p_中的内容soup.p：\n', soup.p)
print('\n获取标签_链接a_中的内容soup.a：\n', soup.a)

all_href = soup.find_all('a')
print('\n获取所有"a标签"的内容soup.find_all(‘a’)：\n', all_href)

print('\n获取某个字典的值_1：')
for a in all_href:
    print(a)
    print(a['href'])

all_href = [a['href'] for a in all_href]
print('\n获取某个字典的值_2：\n', all_href, '\n')




# 加入CSS内容
html = urlopen("https://mofanpy.com/static/scraping/list.html").read().decode('utf-8')
print('\n显示网页的代码信息2：\n\n ----------------开始----------------\n', html, '\n\n----------------结束----------------')  # 显示网页的代码信息

soup = BeautifulSoup(html, features='lxml')  # 把网页放进BeautifulSoup

print('\n利用class筛选出所需要的信息：')
month = soup.find_all('li', {"class": "month"})
print(month, '\n')

print('只显示文本：')
for m in month:
    print(m.get_text())

print('\n 多次筛选：')
january = soup.find('ul', {"class": 'jan'})
print(january, '\n')
d_january = january.find_all('li')  # use january as a parent
print(d_january, '\n')
for d in d_january:
    print(d.get_text())