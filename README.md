# PyJWE
[JSON Web Encryption](https://tools.ietf.org/html/rfc7516) implementation in Python

[![PyPI version](https://badge.fury.io/py/PyJWE.svg)](https://badge.fury.io/py/PyJWE)
[![Build Status](https://travis-ci.org/chrisseto/pyjwe.svg?branch=master)](https://travis-ci.org/chrisseto/pyjwe)


## Basic Usage

```python
import jwe

key = b'MySecretKey'
salt = b'pepper'

derived_key = jwe.kdf(key, salt)

encoded = jwe.encrypt(b'SuperSecretData', derived_key)

print(encoded)

jwe.decrypt(encoded, derived_key)  # b'SuperSecretData'
```


## FAQ

### What is the kdf function? Should I use it? Do I have to use it?

`jwe.kdf` is a very simple [key derivation function](https://en.wikipedia.org/wiki/Key_derivation_function) that uses the [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2).

It is mostly there for the purpose of [key stretching](https://en.wikipedia.org/wiki/Key_stretching) so that users' keys do not have to be the perfect length for AES256.

You do not have to use it, but if you do not your key must be exactly 256 bits.


### Why is `dir` the only algorithm supported?

Because [key wrapping](https://en.wikipedia.org/wiki/Key_Wrap) is more or less [completely useless](https://security.stackexchange.com/questions/40052/when-do-i-use-nist-aes-key-wrapping).


### Why is AES 256 GCM the only encryption methd?

It met my needs and I've yet to need another method.
Feel free to submit an issue if you would like another method implemented.
