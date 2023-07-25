if kx == -pi:
    vector1_array.append(eigenvector[:, 0])
    vector2_array.append(eigenvector[:, 1])
elif kx != pi:
    # 这里的判断是为了处理能带简并时最简单情况，只做个对调。
    if np.abs(np.dot(vector1_array[-1].transpose().conj(), eigenvector[:, 0]))>0.5:
        vector1_array.append(eigenvector[:, 0])
        vector2_array.append(eigenvector[:, 1])
    else:
        vector1_array.append(eigenvector[:, 1])
        vector2_array.append(eigenvector[:, 0])
else:
    # 这里是为了-pi和pi有相同的波函数，使得Wilson loop的值与波函数规范无关。
    vector1_array.append(vector1_array[0])
    vector2_array.append(vector2_array[0])