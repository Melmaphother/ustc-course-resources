import random
with open('../data/plaintext.txt', 'w') as f:
    for i in range(10000):
        f.write(str(random.randint(10000, 1000000000)) + '\n')
