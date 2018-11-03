#!/usr/bin/env python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

"""
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()
"""

requires = [
    'lxml>=3.4.2',
    'picles.plumber>=0.10',
    'python3-bs4',
    'packtools',
    ]

test_requires = ['mocker', 'nose>=1.0', 'coverage', 'mongomock']

setup(
   name='spskit',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=['spskit'],  #same as name
   install_requires=[
    'lxml',
    'picles.plumber>=0.10',
    ], #external packages as dependencies
)
