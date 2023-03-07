.. _install:

Installation
============

This part of the documentation covers the installation of Retask.
The first step to using any software package is getting it properly installed.


Distribute & Pip
----------------

Installing requests is simple with `pip <http://www.pip-installer.org/>`_::

    $ python3 -m pip install retask


Get the Code
------------

Retask is actively developed on GitHub, where the code is
`always available <https://github.com/kushaldas/retask>`_.

You can either clone the public repository::

    git clone git://github.com/kushaldas/retask.git

Download the `tarball <https://github.com/kushaldas/retask/tarball/main>`_::

    $ curl -OL https://github.com/kushaldas/retask/tarball/main

Or, download the `zipball <https://github.com/kushaldas/retask/zipball/main>`_::

    $ curl -OL https://github.com/kushaldas/retask/tarball/main


Then build via using `flit <https://flit.pypa.io/en/latest/index.html>`_ tool.::

    $ flit build

.. _redis:

Installing redis-py
-------------------


You can install ``redis-py`` with ``pip``::

    $ python3 -m pip install redis
