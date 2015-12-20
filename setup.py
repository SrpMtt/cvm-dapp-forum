#!/usr/bin/python3
from setuptools import find_packages
from setuptools import setup

setup(name='forum',
	version='0.1',
	description='forum dapp library',
	author='SrpMtt',
	setup_requires='setuptools',
	package_dir={'':'library'},
	packages=['forum']
)
