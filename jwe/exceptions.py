class PyJWEException(Exception):
    pass


class MalformedData(PyJWEException):
    pass


class MalformedHeader(MalformedData):
    pass


class UnsupportedOption(PyJWEException):
    pass


class UnsupportedAlgorithm(UnsupportedOption):
    pass


class UnsupportedEncryption(UnsupportedOption):
    pass
