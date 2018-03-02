"""
retask Manager implementation

"""

import json
import redis
import uuid
import six
from .task import Task
from .exceptions import ConnectionError

class Manager(object):
    """
    Returns the ``Manager`` object. If the user
    passes optional config dictionary with details for Redis
    server, it will connect to that instance. By default it connects
    to the localhost.

    """
    def __init__(self, config=None):
        specified_config = config or {}
        self.config = {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'password': None,
        }
        self.config.update(specified_config)
        self.rdb = None
        self.connected = False

    def connect(self):
        """
        Creates the connection with the redis server.
        Return ``True`` if the connection works, else returns
        ``False``. It does not take any arguments.

        :return: ``Boolean`` value

        .. note::

           After creating the ``Manager`` object the user should call
           the ``connect`` method to create the connection.

        .. doctest::

           >>> from retask import Manager
           >>> manager = Manager()
           >>> manager.connect()
           True

        """
        config = self.config
        self.rdb = redis.Redis(config['host'], config['port'], config['db'],\
                              config['password'])
        try:
            info = self.rdb.info()
            self.connected = True
        except redis.ConnectionError:
            return False

        return True

    def tasks(self, queue):
        """
        Returns a list of :class:`~retask.task.Task` objects from the given queue.
        Returns ``None`` if the queue is empty.

        :return: list of :class:`~retask.task.Task` objects from the given queue

        If the queue is not connected then it will raise
        :class:`retask.ConnectionError`

        .. doctest::

           >>> from retask import Queue
           >>> from retask import Manager
           >>> q = Queue('test')
           >>> q.connect()
           True
           >>> manager = Manager()
           >>> manager.connect()
           True
           >>> manager.tasks(q)
           [Task({'name': 'Kushal'})]

        """
        if not self.connected:
            raise ConnectionError('Queue is not connected')

        queue_name = queue._name
        queue_length = self.rdb.llen(queue_name)

        if queue_length == 0:
            return None

        queue_tasks = self.rdb.lrange(queue_name, 0, queue_length)
        for index, queue_task in enumerate(queue_tasks):
            if isinstance(queue_task, six.binary_type):
                queue_task = six.text_type(queue_task, 'utf-8', errors = 'replace')
            task = Task()
            task.__dict__ = json.loads(queue_task)
            queue_tasks[index] = task
        return queue_tasks

    def delete(self, queue):
        """
        Deletes a given queue.
        Return ``True`` if the queue exists and is deleted
        ``False``. If no such queue exists

        :return: ``Boolean`` value

        .. doctest::

           >>> from retask import Manager
           >>> manager = Manager()
           >>> manager.connect()
           True
           >>> q = Queue('example')
           >>> q.connect()
           True
           >>> manager.delete(q)
           True
           >>> manager.delete(q)
           False

        """
        if not self.connected:
            raise ConnectionError('Queue is not connected')

        queue_name = queue._name
        status = self.rdb.delete(queue_name)

        if status == 0:
            return False
        return True
