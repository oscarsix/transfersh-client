from setuptools import setup, find_packages
from os import path
from transfersh_client import __VERSION__

here = path.abspath(path.dirname(__file__))


setup(
    name='transfershclient',
    version=__VERSION__,
    packages=['transfersh_client'],
    url='https://github.com/oscarsix/transfersh-client',
    license='MIT',
    author='Oskar Malnowicz',
    author_email='oscarsix@protonmail.ch',
    description='Command line tool for Transfer.sh server',
    scripts=[
        'bin/transfer',
        'bin/transfer-config'
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
)
