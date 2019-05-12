#!/usr/bin/env python

from distutils.core import setup

setup(name='conohactl',
      version='0.1',
      description='Interface for manage VPS on ConoHa',
      author='Yuuki Enomoto',
      author_email='uki@e-yuuki.org',
      license='public domain',
      url='https://github.com/user340/tools/www/conoha',
      package_dir={'': 'src'},
      py_modules=['lib.api', 'lib.cmd', 'lib.exceptions'],
      scripts=['src/conoha.py'],
      install_requires=['yaml', 'requrests', 'texttable']
      )
