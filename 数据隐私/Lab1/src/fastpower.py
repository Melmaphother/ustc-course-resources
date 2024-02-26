def binpow(base, exponent, modulus):
    """TODO: calculate (base^exponent) mod modulus. 
        Recommend to use the fast power algorithm.
    """
    base = base % modulus
    res = 1
    while exponent > 0:
        if (exponent & 1):
            res = res * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return res


if __name__ == "__main__":
    base = 2
    exponent = 10
    modulus = 100
    print(binpow(base, exponent, modulus))
