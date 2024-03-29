import pickle
data = [1, 2, 3]
with open('a.txt', 'wb') as f:
    pickle.dump(data, f)
with open('a.txt', 'rb') as f:
    data_load = pickle.load(f)
print(data_load)