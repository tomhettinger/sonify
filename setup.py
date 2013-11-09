#!/usr/bin/env python
"""Installer script for the sonify module."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='sonify',
      version='0.1.0',
      author='Thomas Hettinger',
      author_email='tomhettinger@gmail.com',
      packages=['sonify', 'tkSnack.tkSnack'],
      scripts=['bin/sonify'],
      url='https://github.com/tomhettinger/sonify',
      license='LICENSE.txt',
      description='An image-to-sound appliction.',
      long_description=open('README.txt').read(),
      install_requires=['nose', 
                        'matplotlib >= 1.1.1', 
                        'PIL >= 1.1.6', 
                        'wavebender == 0.2',
      ],
      dependency_links=['http://github.com/tomhettinger/wavebender/tarball/master#egg=wavebender-0.2']
)
