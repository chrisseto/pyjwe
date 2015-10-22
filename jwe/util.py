from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from jwe.backend import backend


def kdf(key, salt, length=32, iterations=10000):
    return PBKDF2HMAC(
        salt=salt,
        length=length,
        backend=backend,
        iterations=iterations,
        algorithm=hashes.SHA256(),
    ).derive(key)
