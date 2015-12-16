import os
import json
import base64

from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms

from jwe.backend import backend


def base64_urlsafe_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=')


def encrypt(data, key):
    segments = []

    header = {'alg': 'dir', 'enc': 'A256GCM'}
    segments.append(base64_urlsafe_encode(json.dumps(header).encode()))

    segments.append(b'')  # Keywrapping is for suckers

    iv = os.urandom(16)
    segments.append(base64_urlsafe_encode(iv))

    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=backend).encryptor()
    encryptor.authenticate_additional_data(segments[0])
    ciphertext = encryptor.update(data) + encryptor.finalize()
    segments.append(base64_urlsafe_encode(ciphertext))

    segments.append(base64_urlsafe_encode(encryptor.tag))

    return b'.'.join(segments)
