import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range(10), range(10))
ax.set_title('Example', fontsize=20, fontfamily='Times New Roman')
ax.set_xlabel('x', fontsize=20, fontfamily='Times New Roman') 
ax.set_ylabel('y', fontsize=20, fontfamily='Times New Roman')
plt.show()