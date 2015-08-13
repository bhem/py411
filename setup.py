#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path
import io

here = path.abspath(path.dirname(__file__))

NAME = 'py411'
with io.open(path.join(here, NAME, 'version.py'), 'rt', encoding='UTF-8') as f:
    exec(f.read())

setup(
    name=NAME,
    version=__version__,
    setup_requires=['setuptools-markdown'],
    description='A Python library for T411 API requests',
    long_description_markdown_filename='README.md',
    url=__url__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: BSD License',
    ],

    keywords='python api t411 p2p peer download',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['requests'],

    extras_require = {
        'dev': ['check-manifest', 'nose'],
        'test': ['coverage', 'nose'],
    },

    package_data={
        'samples': ['samples/*.py'],
    },
)

