import imageio

images = []
for i in range(1000):
    image = str(i)+'.jpg'
    im = imageio.imread(image)
    images.append(im)
imageio.mimsave("a.gif", images, fps=5, duration=1, loop=0) 

# fps: 帧率，表示每秒显示的帧数。
# duration: 设置每一帧的持续时间（单位：秒），这里设置为 1。
# loop: 设置动图的循环次数，0 表示无限循环。