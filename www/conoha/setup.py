#!/usr/bin/env python

from distutils.core import setup

setup(name='conohactl',
      version='0.1',
      description='Interface for manage VPS on ConoHa',
      author='Yuuki Enomoto',
      author_email='uki@e-yuuki.org',
      url='https://github.com/user340/conohactl',
      package_dir={'': 'src'},
      py_modules=['conoha', 'lib.api', 'lib.cmd']
      )
