import os
import json
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


backend = default_backend()


def kdf(key, salt, length=32, iterations=10000):
    return PBKDF2HMAC(
        salt=salt,
        length=length,
        backend=backend,
        iterations=iterations,
        algorithm=hashes.SHA256(),
    ).derive(key)


def encrypt(data, key):
    segments = []

    header = {'alg': 'dir', 'enc': 'A256GCM'}
    segments.append(base64.b64encode(json.dumps(header).encode()))

    segments.append(b'')  # Keywrapping is for suckers

    iv = os.urandom(16)
    segments.append(base64.b64encode(iv))

    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
    encryptor.authenticate_additional_data(segments[0])
    ciphertext = encryptor.update(data) + encryptor.finalize()
    segments.append(base64.b64encode(ciphertext))

    segments.append(base64.b64encode(encryptor.tag))

    return b'.'.join(segments)


def decrypt(data, key):
    # Generate a random 96-bit IV.
    spl = data.split(b'.')

    try:
        header, _, iv, ciphertext, tag = [base64.b64decode(x) for x in spl]
    except ValueError:
        pass

    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    encryptor.authenticate_additional_data(spl[0])

    return encryptor.update(ciphertext) + encryptor.finalize()
