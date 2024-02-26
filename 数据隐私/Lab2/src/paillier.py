import numpy as np
import phe


class PaillierPublicKey:
    def __init__(self, raw_pub_key):
        self.raw_pub_key = raw_pub_key

    @staticmethod
    def _convert_vector(plain_vector):
        if type(plain_vector) == list:
            plain_vector = plain_vector.copy()  # make a copy

        elif type(plain_vector) == np.ndarray:
            dtype = plain_vector.dtype
            if dtype == np.float64:
                plain_vector = [val for val in plain_vector]
            elif dtype in (np.float16, np.float32):
                plain_vector = [float(val) for val in plain_vector]
            elif dtype in (np.int8, np.int16, np.int32, np.int64):
                plain_vector = [int(val) for val in plain_vector]
            else:
                raise TypeError("python-paillier cannot accept numpy array with {} dtype".format(dtype))

        return plain_vector  # always return a Python list

    def raw_encrypt_vector(self, plain_vector):
        def _encrypt(val):
            # unlike self.raw_encrypt(), there's no need to judge the data type
            return self.raw_pub_key.encrypt(val)

        plain_vector = PaillierPublicKey._convert_vector(plain_vector)
        return [_encrypt(val) for val in plain_vector]


class PaillierPrivateKey:
    def __init__(self, raw_priv_key):
        self.raw_priv_key = raw_priv_key

    def raw_decrypt(self, ciphertext):
        if isinstance(ciphertext, phe.EncryptedNumber):
            return self.raw_priv_key.decrypt(ciphertext)
        else:
            return ciphertext

    def raw_decrypt_vector(self, cipher_vector):
        return [self.raw_decrypt(cipher) for cipher in cipher_vector]


class Paillier:
    def __init__(self, key_size=1024):
        raw_public_key, raw_private_key = self._gen_key(key_size)
        self.pub_key = raw_public_key
        self.priv_key = raw_private_key
        self.pub_key_obj = PaillierPublicKey(raw_public_key)
        self.priv_key_obj = PaillierPrivateKey(raw_private_key)

    def _gen_key(self, key_size):
        pub_key, priv_key = phe.paillier.generate_paillier_keypair(n_length=key_size)
        return pub_key, priv_key

    def encrypt_vector(self, plain_vector):
        return self.pub_key_obj.raw_encrypt_vector(plain_vector)

    def decrypt_vector(self, cipher_vector):
        return self.priv_key_obj.raw_decrypt_vector(cipher_vector)


class PartialPaillier:
    def __init__(self, raw_public_key):
        self.pub_key = raw_public_key
        self.pub_key_obj = PaillierPublicKey(raw_public_key)

    def encrypt_vector(self, plain_vector):
        return self.pub_key_obj.raw_encrypt_vector(plain_vector)


def encode(
    raw_data: np.ndarray,
    raw_pub_key: phe.PaillierPublicKey,
    *,
    precision: float = 0.001,
):
    data_encode = []
    encode_mappings = []
    n_rows, n_cols = raw_data.shape
    for i in range(n_rows):
        encode_vector, vector_mapping = _target_encode(*raw_data[i], raw_pub_key=raw_pub_key, precision=precision)
        data_encode.append(encode_vector)
        encode_mappings.append(vector_mapping)
    return np.array(data_encode), encode_mappings


def _target_encode(*vector, raw_pub_key, precision):
    n, max_int = raw_pub_key.n, raw_pub_key.max_int
    pos_idxs, neg_idxs = [], []
    pos_exps, neg_exps = [], []
    encode_vector = []

    for i, value in enumerate(vector):
        encode_number = phe.EncodedNumber.encode(raw_pub_key, value, precision=precision)
        encode_vector.append(encode_number)
        encoding = encode_number.encoding
        if n - max_int <= encoding:
            neg_idxs.append(i)
            neg_exps.append(n - encoding)
        else:
            pos_idxs.append(i)
            pos_exps.append(encoding)
    vector_mapping = {
        "pos_idxs": pos_idxs,
        "neg_idxs": neg_idxs,
        "pos_exps": pos_exps,
        "neg_exps": neg_exps,
    }

    return encode_vector, vector_mapping
