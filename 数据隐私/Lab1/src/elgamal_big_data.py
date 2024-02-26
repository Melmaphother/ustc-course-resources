import random

import elgamal
import time
from multiprocessing import Pool


def elgamal_encrypt_batch_0(public_key, plaintext):
    p, g, y = public_key
    k = random.randint(1, p - 2)
    c1 = elgamal.mod_exp(g, k, p)
    c3 = elgamal.mod_exp(y, k, p)
    c2 = plaintext * c3 % p
    return (c1, c2), c3


def elgamal_encrypt_batch(public_key, plaintext, c1, c3):
    p = public_key[0]
    c2 = plaintext * c3 % p
    return c1, c2


def elgamal_decrypt_batch_0(public_key, private_key, ciphertext):
    p, g, y = public_key
    c1, c2 = ciphertext
    s = elgamal.mod_exp(c1, private_key, p)
    assert s  # s != 0
    s_1 = elgamal.mod_exp(s, p - 2, p)
    plaintext = c2 * s_1 % p
    return plaintext, s_1


def elgamal_decrypt_batch(public_key, s_1, ciphertext):
    p = public_key[0]
    c2 = ciphertext[1]
    plaintext = c2 * s_1 % p
    return plaintext


def elgamal_batch(plaintexts, public_key, private_key):
    c1, c3, s_1 = 0, 0, 0
    for idx, plaintext in enumerate(plaintexts):
        if idx == 0:
            ciphertext, c3 = elgamal_encrypt_batch_0(public_key, plaintext)
            c1 = ciphertext[0]
            decrypted_text, s_1 = elgamal_decrypt_batch_0(public_key, private_key, ciphertext)
        else:
            ciphertext = elgamal_encrypt_batch(public_key, plaintext, c1, c3)
            decrypted_text = elgamal_decrypt_batch(public_key, s_1, ciphertext)
        assert decrypted_text == plaintext


if __name__ == "__main__":
    # set key_size, such as 256, 1024...
    key_size = int(input("Please input the key size: "))

    # generate keys
    public_key, private_key = elgamal.elgamal_key_generation(key_size)
    print("Public Key:", public_key)
    print("Private Key:", private_key)

    with open('../data/plaintext.txt', 'r') as f:
        plaintexts = f.readlines()
        plaintexts = [int(i.strip()) for i in plaintexts]

    # Encrypt and decrypt one by one
    print("Encrypt and decrypt one by one...")
    T1 = time.perf_counter_ns()
    for plaintext in plaintexts:
        ciphertext = elgamal.elgamal_encrypt(public_key, plaintext)
        decrypted_text = elgamal.elgamal_decrypt(public_key, private_key, ciphertext)
        assert decrypted_text == plaintext
    T2 = time.perf_counter_ns()
    duration = (T2 - T1) / 1e6
    print("Time cost of encrypt and decrypt one by one: {} ms".format(duration))

    # Encrypt and decrypt in batch
    print("Encrypt and decrypt in batch...")
    T1 = time.perf_counter_ns()
    batch_size = 10
    c1, c3, s_1 = 0, 0, 0
    for idx, plaintext in enumerate(plaintexts):
        if idx % batch_size == 0:
            ciphertext, c3 = elgamal_encrypt_batch_0(public_key, plaintext)
            c1 = ciphertext[0]
            decrypted_text, s_1 = elgamal_decrypt_batch_0(public_key, private_key, ciphertext)
        else:
            ciphertext = elgamal_encrypt_batch(public_key, plaintext, c1, c3)
            decrypted_text = elgamal_decrypt_batch(public_key, s_1, ciphertext)
        assert decrypted_text == plaintext
    T2 = time.perf_counter_ns()
    duration = (T2 - T1) / 1e6
    print("Time cost of encrypt and decrypt in batch: {} ms".format(duration))

    # Encrypt and decrypt in batch and multi_processes
    print("Encrypt and decrypt in batch and multi_processes...")
    T1 = time.perf_counter_ns()
    batch_size = 10
    plaintexts = [plaintexts[i:i + batch_size] for i in range(0, len(plaintexts), batch_size)]
    pool = Pool(processes=5)
    for plaintexts_batch in plaintexts:
        pool.apply_async(elgamal_batch, args=(plaintexts_batch, public_key, private_key))
    pool.close()
    T2 = time.perf_counter_ns()
    duration = (T2 - T1) / 1e6
    print("Time cost of encrypt and decrypt in batch and multi_processes: {} ms".format(duration))
