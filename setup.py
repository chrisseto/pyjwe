#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys

from setuptools import find_packages, setup


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version('jwe/__init__.py')


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print(" git tag -a {0} -m 'version {0}'".format(__version__))
    print(' git push --tags')
    sys.exit()

setup(
    name='PyJWE',
    version=__version__,
    description='JSON Web Encryption implementation in Python',
    license='MIT',
    keywords='jwe json encryption token security signing',
    url='http://github.com/chrisseto/pyjwe',
    packages=find_packages(exclude=('test*', 'examples')),
    long_description=read('README.md'),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    install_requires=parse_requirements('requirements.txt')
)
