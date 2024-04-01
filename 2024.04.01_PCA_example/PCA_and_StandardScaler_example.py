import numpy as np
from sklearn.decomposition import PCA

# 创建一个人造数据集，包含10个样本，每个样本有4个特征
X = np.array([[2, 1, 3, 4],
              [3, 5, 2, 8],
              [4, 3, 6, 5],
              [6, 7, 3, 9],
              [5, 4, 7, 6],
              [7, 8, 5, 10],
              [8, 6, 9, 7],
              [9, 10, 6, 11],
              [10, 8, 11, 8],
              [11, 12, 8, 12]])

# 测试一

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()  # 创建StandardScaler对象
X_scaled = scaler.fit_transform(X)  # 对原始数据X进行标准化

pca = PCA() # 创建PCA对象，保留所有主成分
X_transformed = pca.fit_transform(X_scaled) # 对数据进行PCA变换

# 输出原始数据和变换后的数据
print("Original Data:")
print(X)
print(X.shape)
print("\nTransformed Data:")
print(X_transformed)
print(X_transformed.shape)

# 输出各个主成分所解释的方差比例
print("\nExplained Variance Ratio:")
print(pca.explained_variance_ratio_)

print('\n---\n')

# 测试二

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()  # 创建StandardScaler对象
X_scaled = scaler.fit_transform(X)  # 对原始数据X进行标准化

pca = PCA(n_components=2)  # 创建PCA对象，保留前2个主成分
X_transformed = pca.fit_transform(X_scaled)  # 对数据进行PCA变换

# 输出原始数据和变换后的数据
print("Original Data:")
print(X)
print(X.shape)
print("\nTransformed Data:")
print(X_transformed)
print(X_transformed.shape)

# 输出各个主成分所解释的方差比例
print("\nExplained Variance Ratio:")
print(pca.explained_variance_ratio_)