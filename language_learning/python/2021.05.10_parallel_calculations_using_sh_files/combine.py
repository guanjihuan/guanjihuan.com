f = open('combine.txt', 'w')
for job_index in range(7):
    with open('a'+str(job_index)+'.txt', 'r') as f0:
        text = f0.read()
    f.write(text)
f.close()