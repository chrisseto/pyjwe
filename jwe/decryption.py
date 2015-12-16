import json
import base64

from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms

from jwe import exceptions
from jwe.backend import backend
from jwe.validation import validate_header


def base64_urlsafe_decode(data):
    return base64.urlsafe_b64decode(data + (b'=' * (len(data) % 4)))


def decrypt(data, key):
    spl = data.split(b'.')

    try:
        header, encrypted_key, iv, ciphertext, tag = [base64_urlsafe_decode(x) for x in spl]
    except ValueError:
        raise exceptions.MalformedData('Recieved incorrected formatted data. Expected 5 segments, received {}'.format(len(spl)))

    if encrypted_key:
        raise exceptions.UnsupportedOption('Key wrapping is currently not supported')

    try:
        validate_header(json.loads(header.decode('utf-8')))
    except ValueError:
        raise exceptions.MalformedData('Header is not valid JSON')

    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=backend
    ).decryptor()

    encryptor.authenticate_additional_data(spl[0])

    return encryptor.update(ciphertext) + encryptor.finalize()
