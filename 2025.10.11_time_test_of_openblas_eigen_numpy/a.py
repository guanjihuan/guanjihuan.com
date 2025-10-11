import numpy as np
import time

sizes = [100, 200, 300, 500, 1000, 2000, 3000, 5000]
trials = 3

for size in sizes:
    print(f"Testing size: {size}x{size}")
    
    A = np.random.rand(size, size)
    A = A.T @ A + np.eye(size)
    
    start = time.time()
    
    for _ in range(trials):
        A_inv = np.linalg.inv(A)
    
    end = time.time()
    duration = end - start
    
    print(f"Average time per inversion: {duration/trials:.3f} s")
    print("----------------------------------")