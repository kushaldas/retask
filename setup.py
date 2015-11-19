#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import find_packages, setup

setup(name='retask',
      version='0.4',
      description='Task Queue implementation in python',
      long_description=(
          'Retask is a simple task queue implementation written for '
          'human beings. It provides generic solution to create and manage '
          'task queues.'
      ),
      author='Kushal Das',
      author_email='kushaldas@gmail.com',
      maintainer='Kushal Das',
      maintainer_email='kushaldas@gmail.com',
      license='MIT',
      url='https://github.com/kushaldas/retask',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Topic :: System :: Distributed Computing',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2'
          ],
      packages=find_packages(),
      data_files=[],
      install_requires=[
          'redis',
          'six'
      ],
      test_suite='tests',
      tests_require=[
          'mock'
      ])
