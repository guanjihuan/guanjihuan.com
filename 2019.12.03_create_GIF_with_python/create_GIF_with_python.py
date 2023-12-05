import imageio

images = []
for i in range(1000):
    image = str(i)+'.jpg'
    im = imageio.imread(image)
    images.append(im)
imageio.mimsave("a.gif", images, 'GIF', duration=0.1)  # durantion是延迟时间