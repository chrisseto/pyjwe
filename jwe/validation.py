from jwe import exceptions


REQUIRED_HEADER_KEYS = ('alg', 'enc')
SUPPORTED_ENCRYPTIONS = ('A256GCM', )
SUPPORTED_ALGORITHMS = ('dir', )


def validate_header(header):
    for key in REQUIRED_HEADER_KEYS:
        if key not in header:
            raise exceptions.MalformedHeader('"{}" missing from header.'.format(key))

    if header['alg'] not in SUPPORTED_ALGORITHMS:
        raise exceptions.UnsupportedAlgorithm(header['alg'])

    if header['enc'] not in SUPPORTED_ENCRYPTIONS:
        raise exceptions.UnsupportedEncryption(header['enc'])
