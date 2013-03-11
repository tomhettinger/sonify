#!/usr/bin/env python
"""
Installer script for the sonify module.
"""

from distutils.core import setup
import sonify

setup (
    name = 'sonify',
    version = 0.1.0,
    author = 'Thomas Hettinger'
    author_email = 'tomhettinger@gmail.com'
    packages = ['sonify',],
    scripts = ['bin/sonify-gui.py'],
    url = 'https://github.com/tomhettinger/sonify',
    license='LICENSE.txt',
    description = 'An image-to-sound appliction.',
    long_description = open('README.txt').read(),
    install_requires = ["wavebender == 0.2",
                        "matplotlib >= ??",],
)
