# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Sample Odoo ETL Package For Crea',
    long_description=readme,
    author='Jeffery M. Cooper',
    author_email='jmc.dev.1968@gmail.com',
    url='https://github.com/jmc-dev-1968/crea',
    packages=find_packages(exclude=('tests', 'docs'))
)

