import numpy as np
import matplotlib.pyplot as plt

def sigmoid_function(x):
    y = 1/(1+np.exp(-x))
    return y

for num in [5, 10, 20, 30, 40, 50, 100, 200, 300]:
    x_array = np.linspace(-10, 10, num)
    y_array = []
    for x in x_array:
        y = sigmoid_function(x)
        y_array.append(y)
    plt.plot(x_array, y_array, 'o-')
    plt.title(f'Num={num}')
    plt.show()