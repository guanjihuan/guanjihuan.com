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
match_href = []
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
            match_href.append(href)
# 对链接进行排序并写入文件
numbers = []
match_href_new = [] 
for href in match_href:
    numbers.append(int(href[29:]))
numbers.sort(reverse = True)
for n in numbers:
    match_href_new.append('https://zhuanlan.zhihu.com/p/'+str(n))

# 获取内容并写入文件
f = open('zhihu.html', 'w', encoding='UTF-8') 
f.write('<meta charset="utf-8"><style type="text/css">a{text-decoration: none;color: #0a5794;}a:hover {text-decoration: underline;color: red; }</style>')
f.write('<p>'+str(year)+'.'+str(month).rjust(2,'0')+'.'+str(day).rjust(2,'0')+' 已更新</p>')
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
f.close()
