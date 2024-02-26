import random
import time
import test_sympy


def is_primitive_root(g, p, factors):  # 原根判定定理
    # determine whether g is a primitive root of p
    for factor in factors:
        if pow(g, (p - 1) // factor, p) == 1:
            return False
    return True


def generate_p_and_g(n_bit):
    while True:
        # generate an n-bit random prime number p
        p = sympy.randprime(2 ** (n_bit - 1), 2 ** n_bit)

        # compute the prime factorization of p-1
        factors = sympy.factorint(p - 1).keys()

        # choose a possible primitive root g
        for g in range(2, p):
            if is_primitive_root(g, p, factors):
                return p, g


def mod_exp(base, exponent, modulus):
    """
    快速幂算法的经典python实现
    """
    base = base % modulus
    result = 1
    while exponent > 0:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def elgamal_key_generation(key_size):
    """Generate the keys based on the key_size.
    经典的随机数生成算法，生成一个大素数 p 和一个原根 g
    """
    # generate a large prime number p and a primitive root g
    p, g = generate_p_and_g(key_size)

    # TODO: generate x and y here.
    assert p - 2 >= 1
    x = random.randint(1, p - 2)
    y = mod_exp(g, x, p)

    return (p, g, y), x


def elgamal_encrypt(public_key, plaintext):
    """TODO: encrypt the plaintext with the public key.
    """
    p, g, y = public_key
    k = random.randint(1, p - 2)
    c1 = mod_exp(g, k, p)
    c2 = plaintext * mod_exp(y, k, p) % p
    return c1, c2


def elgamal_decrypt(public_key, private_key, ciphertext):
    """TODO: decrypt the ciphertext with the public key and the private key.
    """
    p, g, y = public_key
    c1, c2 = ciphertext
    s = mod_exp(c1, private_key, p)
    assert s  # s != 0
    plaintext = c2 * mod_exp(s, p - 2, p) % p
    return plaintext


if __name__ == "__main__":
    # set key_size, such as 256, 1024...
    key_size = int(input("Please input the key size: "))

    # generate keys
    T1 = time.perf_counter_ns()
    public_key, private_key = elgamal_key_generation(key_size)
    T2 = time.perf_counter_ns()
    duration = (T2 - T1) / 1e6
    print("Key_size {}, Key generation time {} ms".format(key_size, duration))
    print("Public Key:", public_key)
    print("Private Key:", private_key)

    # encrypt plaintext
    plaintext = int(input("Please input an integer: "))
    ciphertext = elgamal_encrypt(public_key, plaintext)
    print("Ciphertext:", ciphertext)

    # decrypt ciphertext
    decrypted_text = elgamal_decrypt(public_key, private_key, ciphertext)
    print("Decrypted Text:", decrypted_text)
