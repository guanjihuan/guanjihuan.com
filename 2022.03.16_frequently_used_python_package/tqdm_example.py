from tqdm import tqdm 
import time
import numpy as np

for i in tqdm(np.arange(1, 10)):     
    time.sleep(0.1)
    print('', i)