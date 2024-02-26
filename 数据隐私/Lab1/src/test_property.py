import elgamal
import time

if __name__ == "__main__":
    # set key_size, such as 256, 1024...
    key_size = int(input("Please input the key size: "))

    # generate keys
    public_key, private_key = elgamal.elgamal_key_generation(key_size)
    print("Public Key:", public_key)
    print("Private Key:", private_key)

    # Verify the randomness of the ElGamal algorithm
    print("Verify the randomness of the ElGamal algorithm")
    # encrypt plaintext
    plaintext = int(input("Please input the plaintext: "))
    ciphertext_1 = elgamal.elgamal_encrypt(public_key, plaintext)
    print("The First ciphertext:", ciphertext_1)
    ciphertext_2 = elgamal.elgamal_encrypt(public_key, plaintext)
    print("The Second ciphertext:", ciphertext_2)
    if ciphertext_1 != ciphertext_2:
        print("The randomness of the ElGamal algorithm is correct!")
    else:
        print("The randomness of the ElGamal algorithm is wrong!")

    # Verifying the multiplicative homomorphism of the ElGamal algorithm
    print("Verifying the multiplicative homomorphism of the ElGamal algorithm")
    plaintext_1 = int(input("Please input the first plaintext: "))
    plaintext_2 = int(input("Please input the second plaintext: "))
    ciphertext_1 = elgamal.elgamal_encrypt(public_key, plaintext_1)
    ciphertext_2 = elgamal.elgamal_encrypt(public_key, plaintext_2)

    # unencrypted the ciphertexts and multiply them
    T1 = time.perf_counter_ns()
    decrypted_text_1 = elgamal.elgamal_decrypt(public_key, private_key, ciphertext_1)
    decrypted_text_2 = elgamal.elgamal_decrypt(public_key, private_key, ciphertext_2)
    multiplication = decrypted_text_1 * decrypted_text_2
    T2 = time.perf_counter_ns()
    duration_1 = (T2 - T1) / 1e6
    print("The First decrypted text:", decrypted_text_1)
    print("The Second decrypted text:", decrypted_text_2)
    print("The multiplication of the decrypted text:", multiplication)

    # unencrypted the multiplication of the ciphertext
    T1 = time.perf_counter_ns()
    decrypted_text = elgamal.elgamal_decrypt(public_key, private_key,
                                             (ciphertext_1[0] * ciphertext_2[0], ciphertext_1[1] * ciphertext_2[1]))
    T2 = time.perf_counter_ns()
    duration_2 = (T2 - T1) / 1e6
    print("The decrypted text of the multiplication of the ciphertext:", decrypted_text)

    # Compare
    print("Compare")
    if decrypted_text_1 * decrypted_text_2 == decrypted_text:
        print("The multiplicative homomorphism of the ElGamal algorithm is correct!")
    else:
        print("The multiplicative homomorphism of the ElGamal algorithm is wrong!")
    print("The duration of unencrypted the ciphertexts and multiply them: ", duration_1, "ms")
    print("The duration of unencrypted the multiplication of the ciphertext: ", duration_2, "ms")
