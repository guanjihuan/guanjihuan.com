"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/44839
"""

import os
os.environ["OMP_NUM_THREADS"] = "1" # KMeans is known to have a memory leak on Windows with MKL, when there are less chunks than available threads. You can avoid it by setting this environment variable

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

X, y = make_blobs(n_samples=300, centers=4, random_state=42) # 生成示例数据（四类）
print(X.shape)
print(y.shape)
plt.scatter(X[:, 0], X[:, 1]) # 显示数据
plt.show()

plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis') # 通过颜色显示数据原有的标签
plt.show()

kmeans = KMeans(n_clusters=3, random_state=42) # 进行 KMeans 聚类（这里分为三类）
kmeans.fit(X)
labels = kmeans.labels_  # 获取聚类的标签
print(labels.shape)

plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis') # 绘制聚类结果
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red', marker='X') # 绘制聚类中心
plt.title('KMeans Result')
plt.show()