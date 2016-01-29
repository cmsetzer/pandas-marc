#!/usr/bin/env python3

"""Setup and installation script for pandas-marc."""

from setuptools import setup

setup(name='pandas-marc',
      version='0.1.0',
      description='A tool for working with MARC metadata in pandas dataframes',
      py_modules=['pandas_marc'],
      install_requires=['pandas', 'pymarc'])
