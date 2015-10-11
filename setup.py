#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import find_packages, setup


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


version = '0.1.1'
requirements = parse_requirements('requirements.txt')

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print(" git tag -a {0} -m 'version {0}'".format(version))
    print(' git push --tags')
    sys.exit()

tests_require = [
    'pytest==2.7.3',
    'pytest-cov',
    'pytest-runner',
]

needs_pytest = set(('pytest', 'test', 'ptr')).intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup(
    name='PyJWE',
    version=version,
    description='JSON Web Encryption implementation in Python',
    license='MIT',
    keywords='jwe json encryption token security signing',
    url='http://github.com/chrisseto/pyjwe',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    long_description=long_description,
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
    setup_requires=pytest_runner,
    tests_require=tests_require,
    install_requires=requirements,
    extras_require=dict(
        test=tests_require,
        crypto=['cryptography'],
        flake8=[
            'flake8',
            'flake8-import-order',
            'pep8-naming'
        ]
    ),
)
