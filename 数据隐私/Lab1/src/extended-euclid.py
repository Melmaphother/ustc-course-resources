
def ExtendedEuclid(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        (d, x, y) = ExtendedEuclid(b, a % b)
        # print(d, x, y)
        return (d, y, x-(a//b)*y)


print(ExtendedEuclid(99, 78))

