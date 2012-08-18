.. _install:

Installation
============

This part of the documentation covers the installation of Retask.
The first step to using any software package is getting it properly installed.


Distribute & Pip
----------------

Installing requests is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install retask

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install retask

But, you really `shouldn't do that <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.



Get the Code
------------

Retask is actively developed on GitHub, where the code is
`always available <https://github.com/kushaldas/retask>`_.

You can either clone the public repository::

    git clone git://github.com/kushaldas/retask.git

Download the `tarball <https://github.com/kushaldas/retask/tarball/master>`_::

    $ curl -OL https://github.com/kushaldas/retask/tarball/master

Or, download the `zipball <https://github.com/kushaldas/retask/zipball/master>`_::

    $ curl -OL https://github.com/kushaldas/retask/tarball/master


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install

.. _redis:

Installing redis-py
-------------------


You can install ``redis-py`` with ``pip``::

    $ pip install redis
