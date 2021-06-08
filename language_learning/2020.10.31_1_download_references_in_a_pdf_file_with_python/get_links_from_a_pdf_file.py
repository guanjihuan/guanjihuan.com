"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6869
"""

import PyPDF2
import os
import re 

os.chdir('D:/')  # PDF文件存放的位置
filename = input('输入PDF文件名：')
pdfFile = open(filename+'.pdf','rb')
pdfReader = PyPDF2.PdfFileReader(pdfFile)
pages = pdfReader.getNumPages()
i0 = 0
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
                        i0 += 1
                        old = u['/A']['/URI']        
pdfFile.close()