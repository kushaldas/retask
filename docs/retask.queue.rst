:mod:`retask.queue`
=======================
This module contains the primary :class:`Queue` which 
can be used to create and manage queues.

.. class:: Queue(name, [config={}])

   Returns the ``Queue`` object with the given name. If the user
   passes optional config dictionary with details for Redis
   server, it will connect to that instance. By default it connects
   to the localhost.


   .. method:: connect()

      Creates the connection with the redis server.
      Return ``True`` if the connection works, else returns
      ``False``. It does not take any arguments.

      .. note::

         After creating the ``Queue`` object the user should call
         the ``connect`` method so create the connection.

      .. doctest::

         >>> from retask.queue import Queue
         >>> q = Queue('test')
         >>> q.connect()
         True

   .. method:: enqueue(task)

      Enqueues the given :class:`Task` object to the queue and returns
      a tuple. Value in index 0 is ``Boolean`` explaining the enqueue
      operation is a success or not. Value at index 1 is string with 
      error/success message (if any).

      .. doctest::

         >>> from retask.queue import Queue
         >>> q = Queue('test')
         >>> q.connect()
         True
         >>> from retask.task import Task
         >>> task = Task({'name':'kushal'})
         >>> q.enqueue(task)
         (True, 'Pushed')


   .. method:: dequeue()

      Returns a :class:`Task` object from the queue. Returns ``None`` if the
      queue is empty.

      .. doctest::

         >>> from retask.queue import Queue
         >>> q = Queue('test')
         >>> q.connect()
         True
         >>> t = q.dequeue()
         >>> print t.data
         {u'name': u'kushal'}


      .. data:: length

         Gives the length of the queue. Returns ``None`` if the queue is not
         connected.
