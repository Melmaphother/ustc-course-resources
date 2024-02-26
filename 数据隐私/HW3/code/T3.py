n = 11413
e = 3533
d = 1
for i in range(2, 11200):
    if (3533 * i) % 11200 == 1:
        d = i
        break

m = 9726
c = m
for i in range(1, e):
    c = c * m % n

print(c)

m_decrypt = c
for i in range(1, d):
    m_decrypt = m_decrypt * c % n

print(m_decrypt)

assert m_decrypt == m
