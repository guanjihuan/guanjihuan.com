import time

start_time = time.time()
for _ in range(10**8):
    pass
end_time = time.time()
print(end_time-start_time)

start_time = time.time()
for _ in range(10**6):
    for _ in range(10**2):
        pass
end_time = time.time()
print(end_time-start_time)

start_time = time.time()
for _ in range(10**4):
    for _ in range(10**2):
        for _ in range(10**2):
            pass
end_time = time.time()
print(end_time-start_time)

print('---')

for num in range(11):
    times = 10**num
    start_time = time.time()
    for _ in range(times):
        pass
    end_time = time.time()
    print(f'10^{num}: {end_time-start_time}')