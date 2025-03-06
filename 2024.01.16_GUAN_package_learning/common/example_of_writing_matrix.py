# 矩阵写入文件后查看
import guan
import numpy as np
matrix = np.random.rand(5, 5)
guan.write_matrix_in_markdown_format(matrix=matrix, filename='markdown_matrix')
guan.write_matrix_in_latex_format(matrix=matrix, filename='latex_matrix')