# -*- coding: utf-8 -*-

"""
retask.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Retask's exceptions.

"""

class RetaskException(RuntimeError):
    """Some ambiguous exception occurred"""

class ConnectionError(RetaskException):
    """A Connection error occurred."""
