import imageio
import numpy as np
import os
os.chdir('D:/data')  # 设置文件读取和保存位置

images = []
for i in range(1000):
    image = str(i)+'.jpg'
    im = imageio.imread(image)
    images.append(im)
imageio.mimsave("a.gif", images, 'GIF', duration=0.1)  # durantion是延迟时间