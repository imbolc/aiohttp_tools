#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages


def read(filename):
    with open(filename, 'rt') as f:
        return f.read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit(0)


setup(
    name='aiohttp_tools',
    version='0.0.1',

    description='A set of little tools for aiohttp-based sites',
    long_description=read('README.rst'),

    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],

    author='Imbolc',
    author_email='imbolc@imbolc.name',
    license='ISC',
    url='https://github.com/imbolc/aiohttp_tools',

    packages=find_packages(),
)
