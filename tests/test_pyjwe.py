import pytest

import jwe
from jwe import validation

from cryptography.exceptions import InvalidTag


class TestValidation:

    def test_correct_header(self):
        try:
            validation.validate_header({
                'alg': 'dir',
                'enc': 'A256GCM'
            })
        except Exception as e:
            pytest.fail(e)

    def test_missing_keys(self):
        with pytest.raises(jwe.exceptions.MalformedHeader):
            validation.validate_header({})

    def test_missing_alg(self):
        with pytest.raises(jwe.exceptions.MalformedHeader):
            validation.validate_header({'alg': 'dir'})

    def test_missing_enc(self):
        with pytest.raises(jwe.exceptions.MalformedHeader):
            validation.validate_header({'enc': 'A256GCM'})

    def test_unsupported_alg(self):
        with pytest.raises(jwe.exceptions.UnsupportedAlgorithm):
            validation.validate_header({'alg': 'foo', 'enc': 'A256GCM'})
        with pytest.raises(jwe.exceptions.UnsupportedAlgorithm):
            validation.validate_header({'alg': 'bar', 'enc': 'A256GCM'})
        with pytest.raises(jwe.exceptions.UnsupportedAlgorithm):
            validation.validate_header({'alg': 'baz', 'enc': 'A256GCM'})

    def test_unsupported_enc(self):
        with pytest.raises(jwe.exceptions.UnsupportedEncryption):
            validation.validate_header({'alg': 'dir', 'enc': 'RSA'})
        with pytest.raises(jwe.exceptions.UnsupportedEncryption):
            validation.validate_header({'alg': 'dir', 'enc': 'A126'})
        with pytest.raises(jwe.exceptions.UnsupportedEncryption):
            validation.validate_header({'alg': 'dir', 'enc': 'Base64'})


class TestApi:

    def test_encrypt_decrypt(self):
        key = jwe.kdf(b'Testing', b'Pepper')
        data = b'Just some data'
        encrypted = jwe.encrypt(data, key)

        assert encrypted != data
        assert jwe.decrypt(encrypted, key) == data

    def test_improper_key(self):
        key = jwe.kdf(b'Testing', b'Pepper')
        data = b'Just some data'
        encrypted = jwe.encrypt(data, key)

        with pytest.raises(InvalidTag):
            # TODO make this a custom exception
            jwe.decrypt(encrypted, jwe.kdf(b'somekey', b'Salt')) == data


class TestDecryption:

    def test_invalid_data(self):
        with pytest.raises(jwe.exceptions.MalformedData):
            jwe.decrypt(b'junkdata', jwe.kdf(b'key', b'Salt'))

    def test_invalid_header_json(self):
        with pytest.raises(jwe.exceptions.MalformedData) as e:
            jwe.decrypt(
                jwe.encrypt(
                    b'Just Some Data',
                    jwe.kdf(b'key', b'Salt')
                )[3:],  # Cut out some of the JSON
                jwe.kdf(b'key', b'Salt')
            )

        assert e.value.args[0] == 'Header is not valid JSON'

    def test_no_key_wrapping(self):
        data = jwe.encrypt(b'Just Some Data', jwe.kdf(b'key', b'Salt')).split(b'.')
        data[1] = b'cmFwcGE='

        with pytest.raises(jwe.exceptions.UnsupportedOption) as e:
            jwe.decrypt(b'.'.join(data), jwe.kdf(b'key', b'Salt'))

        assert e.value.args[0] == 'Key wrapping is currently not supported'
