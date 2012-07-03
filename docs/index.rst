.. retask documentation master file, created by
   sphinx-quickstart on Tue Jul  3 14:56:38 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to retask's documentation!
==================================
retask is a python module to create and manage distributed task queues.

It uses `Redis <http://redis.io>` to create task queues. User can enqueue
 and dequeue tasks in the queues they manage. Each task can contain any 
 serializable python objects. We use `JSON` internally to store the tasks
 in the queues.

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

