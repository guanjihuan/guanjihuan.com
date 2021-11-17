"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/17937
"""


from bs4 import BeautifulSoup
from urllib.request import urlopen
import re  
import datetime

year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day

# 获取链接
try:
    with open('link_list.txt', 'r', encoding='UTF-8') as f:  # 如果文件存在
        link_list = f.read().split('\n')   # 历史已经访问过的链接（数组类型）
except:
    with open('link_list.txt', 'w', encoding='UTF-8') as f:  # 如果文件不存在
        link_list = [] 
f = open('link_list.txt', 'a', encoding='UTF-8')  # 打开文件（补充）
f.write('\nLink list obtained on '+str(year)+'.'+str(month).rjust(2,'0')+'.'+str(day).rjust(2,'0')+':\n')
match_href = []  # 在本次运行中满足条件的链接

# 由于没有模拟登录知乎，因此只能爬取到最新的两篇专栏博文
authors = ["https://www.zhihu.com/people/g3508/posts", # Guan
]
for i0 in range(len(authors)):
    start_link = authors[i0]
    html = urlopen(start_link).read().decode('utf-8')  # 打开网页
    soup = BeautifulSoup(html, features='lxml') # 放入soup中
    all_a_tag = soup.find_all('a', href=True)  # 获取超链接标签
    for a_tag in all_a_tag:
        href = a_tag['href']  # 超链接字符串
        if re.search('//zhuanlan.zhihu.com/p/', href): # 文章的链接
            if re.search('https:', href)==None:  # 如果链接不是完整的，那么补充完整
                href = 'https:'+ href
            if href not in match_href and href not in link_list and re.search('\?', href)==None:  # 链接不重复
                match_href.append(href)
# 对链接进行排序并写入文件
numbers = []
match_href_new = [] 
for href in match_href:
    numbers.append(int(href[29:]))
numbers.sort(reverse = True)
for n in numbers:
    f.write('https://zhuanlan.zhihu.com/p/'+str(n)+'\n')
    match_href_new.append('https://zhuanlan.zhihu.com/p/'+str(n))
f.close()


# 获取内容并写入文件
try:
    f_before = open('zhihu.txt', 'r', encoding='UTF-8')
    data = f_before.read()
    f = open('zhihu.txt', 'w', encoding='UTF-8') 
except:
    f = open('zhihu.txt', 'w', encoding='UTF-8') 
for href in match_href_new: 
    try:
        html = urlopen(href).read().decode('utf-8')   # 打开文章链接
        soup = BeautifulSoup(html, features='lxml') # 放入soup中
        title = soup.title   # 文章标题
        f.write('<p><a target=\"_blank\" href=\"')
        f.write(str(href))   # 文章链接
        f.write('\">')
        f.write(str(title.get_text()))
        f.write('</a>&nbsp;&nbsp;') 
        author = soup.find("span", {"class": "UserLink AuthorInfo-name"})
        f.write(str(author.get_text()+'&nbsp;&nbsp;'))
        post_time = soup.find("div", {"class" : "ContentItem-time"})
        f.write(str(post_time.get_text())+'</p>')
        
    except:
        pass
try:
    f.write(data)
    f_before.close()
except:
    pass
f.close()

# 制作HTML
f_html = open('zhihu.html', 'w', encoding='UTF-8')
f_html.write('<meta charset="utf-8">')
f = open('zhihu.txt', 'r', encoding='UTF-8')
data = f.read()
f_html.write(data)
f.close()
f_html.close()
