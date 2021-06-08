"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6869
"""

import PyPDF2
import os
import re 
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests



def main():
    os.chdir('D:/')  # PDF文件存放的位置
    filename = input('输入PDF文件名：')
    pdfFile = open(filename+'.pdf','rb')  # 打开PDF文件
    links = all_links_in_pdf(pdfFile)  # 获取PDF文件中的链接
    pdfFile.close()  # 关闭PDF文件
    os.chdir('D:/Reference')  # 设置参考文献保存的位置
    download(links)  # 下载文献



def all_links_in_pdf(pdfFile): 
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    pages = pdfReader.getNumPages()
    i0 = 0
    links = []
    print()
    for page in range(pages):
        pageSliced = pdfReader.getPage(page)
        pageObject = pageSliced.getObject()
        if '/Annots' in pageObject.keys():
            ann = pageObject['/Annots']
            old = ''
            for a in ann:
                u = a.getObject()
                if '/A' in u.keys():
                    if re.search(re.compile('^https://doi.org'), u['/A']['/URI']):   # 排除其他形式的链接
                        if u['/A']['/URI'] != old: # 排除重复链接
                            print(i0 , u['/A']['/URI'])
                            links.append(u['/A']['/URI']) # 链接存在link数组中 
                            i0 += 1
                            old = u['/A']['/URI']        
    return links



def download(links):
    for i0 in [0, 1, 3]:  # 指定参考文献下载，如需全部下载用for i0 in range(links.shape[0]):
        address = links[i0]
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
        print('\n正在下载第',i0,'篇')
        r = requests.get(pdf_URL, stream=True)
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)
        print('第',i0,'篇下载完成！')
    print('\n全部下载完成！')


if __name__ == '__main__':
    main()