"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/39029
"""

import torch
import numpy as np
import matplotlib.pyplot as plt

x_array = np.linspace(-6, 6, 100)
x_array_torch_tensor = torch.from_numpy(x_array)

y_array_torch_tensor = torch.nn.functional.sigmoid(x_array_torch_tensor)
plt.plot(x_array_torch_tensor, y_array_torch_tensor)
plt.title('sigmoid')
plt.show()

y_array_torch_tensor = torch.nn.functional.tanh(x_array_torch_tensor)
plt.plot(x_array_torch_tensor, y_array_torch_tensor)
plt.title('tanh')
plt.show()

y_array_torch_tensor = torch.nn.functional.relu(x_array_torch_tensor)
plt.plot(x_array_torch_tensor, y_array_torch_tensor)
plt.title('relu')
plt.show()

y_array_torch_tensor = torch.nn.functional.leaky_relu(x_array_torch_tensor)
plt.plot(x_array_torch_tensor, y_array_torch_tensor)
plt.title('leaky_relu')
plt.show()

y_array_torch_tensor = torch.nn.functional.gelu(x_array_torch_tensor)
plt.plot(x_array_torch_tensor, y_array_torch_tensor)
plt.title('gelu')
plt.show()

y_array_torch_tensor = torch.nn.functional.silu(x_array_torch_tensor)
plt.plot(x_array_torch_tensor, y_array_torch_tensor)
plt.title('silu')
plt.show()