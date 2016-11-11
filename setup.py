#!/usr/bin/env python3

from setuptools import setup

setup(name='vagga2lithos',
      version='0.1.0',
      description='A tool that generates lithos configs from vagga configs',
      author='Paul Colomiets',
      author_email='paul@colomiets.name',
      url='http://github.com/tailhook/vagga2lithos',
      packages=['vagga2lithos'],
      install_requires=[
        'PyYaml',
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      )
