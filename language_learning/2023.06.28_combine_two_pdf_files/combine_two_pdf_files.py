"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/34649
"""

import PyPDF2

# 创建一个空的PDF对象
output_pdf = PyPDF2.PdfWriter()

# 打开第一个PDF文件
with open('a.pdf', 'rb') as file1:
    pdf1 = PyPDF2.PdfReader(file1)
    
    # 将第一个PDF文件的所有页面添加到输出PDF对象中
    for page in range(len(pdf1.pages)):
        output_pdf.add_page(pdf1.pages[page])
    
# 打开第二个PDF文件
with open('b.pdf', 'rb') as file2:
    pdf2 = PyPDF2.PdfReader(file2)
    
    # 将第二个PDF文件的所有页面添加到输出PDF对象中
    for page in range(len(pdf2.pages)):
        output_pdf.add_page(pdf2.pages[page])
        
# 保存合并后的PDF文件
with open('combined_file.pdf', 'wb') as merged_file:
    output_pdf.write(merged_file)



# import guan
# guan.combine_two_pdf_files(input_file1='a.pdf', input_file2='b.pdf', output_file='combined_file.pdf')