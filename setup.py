#!/usr/bin/env python
"""Installer script for the sonify module."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'sonify',
    'version': '0.1.0',
    'author': 'Thomas Hettinger',
    'author_email': 'tomhettinger@gmail.com',
    'packages': ['sonify',],
    'scripts': ['bin/sonify'],
    'url': 'https://github.com/tomhettinger/sonify',
    'license': 'LICENSE.txt',
    'description': 'An image-to-sound appliction.',
    'long_description': open('README.txt').read(),
    'install_requires': ['nose', 'wavebender == 0.2', 'matplotlib >= 1.1.1',],
}

setup(**config)
