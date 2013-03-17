#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import find_packages, setup
import retask.release as rl

setup(name='retask',
      version=rl.VERSION,
      description=rl.DESCRIPTION,
      long_description=rl.LONG_DESCRIPTION,
      author=rl.AUTHOR,
      author_email=rl.EMAIL,
      maintainer='Kushal Das',
      maintainer_email='kushaldas@gmail.com',
      license=rl.LICENSE,
      url=rl.URL,
      classifiers=[
          'Development Status :: 4 - Beta',
          
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Topic :: System :: Distributed Computing',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7'
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
      ]
)

