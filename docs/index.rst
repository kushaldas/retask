.. retask documentation master file, created by
   sphinx-quickstart on Tue Jul  3 14:56:38 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Retask: simple Task Queue
=============================
retask is a python module to create and manage distributed task queues.

It uses `Redis <http://redis.io>`_ to create task queues. User can enqueue
and dequeue tasks in the queues they manage. Each task can contain any 
serializable python objects. We use `JSON` internally to store the tasks
in the queues.

Dependencies
------------
- python-redis
- mock
- A running Redis server


Setting up the Redis Server
---------------------------
You can download and install `Redis <http://redis.io>`_ on your distro.
In `Fedora <http://fedoraproject.org>`_ you can just ``yum install redis``
for the same.

To start the server in the local folder use the following command:

::

    $ redis-server

On Fedora you can start the service as *root*:

::

    # service redis start

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   retask.task
   retask.queue


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

