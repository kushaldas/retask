#Copyright (C) 2012, Kushal Das <kushaldas@gmail.com>

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

__author__ = 'Kushal Das <kushaldas@gmail.com'
__copyright__ = 'Copyright (c) 2012 Kushal Das'
__license__ = 'MIT'
__status__ = 'Development'
__version__ = '0.2'

"""
retask Queue implementation

"""
import json
import redis
import uuid
from task import Task
from exceptions import ConnectionError


class Queue(object):
    """
    Returns the ``Queue`` object with the given name. If the user
    passes optional config dictionary with details for Redis
    server, it will connect to that instance. By default it connects
    to the localhost.

    """
    def __init__(self, name, config={}):
        self.name = name
        self._name = 'retaskqueue-' + name
        if not config:
            self.config = {'host': 'localhost', 'port': 6379, 'db': 0,\
                           'password': None}
        else:
            self.config = config
        self.rdb = None
        self.connected = False

    @property
    def length(self):
        """
        Gives the length of the queue. Returns ``None`` if the queue is not
        connected.

        If the queue is not connected then it will raise
        :class:`retask.ConnectionError`.

        """
        if not self.connected:
            raise ConnectionError('Queue is not connected')

        try:
            length = self.rdb.llen(self._name)
        except redis.exceptions.ConnectionError, err:
            raise ConnectionError(str(err))

        return length

    def connect(self):
        """
        Creates the connection with the redis server.
        Return ``True`` if the connection works, else returns
        ``False``. It does not take any arguments.

        :return: ``Boolean`` value

        .. note::

           After creating the ``Queue`` object the user should call
           the ``connect`` method so create the connection.

        .. doctest::

           >>> from retask.queue import Queue
           >>> q = Queue('test')
           >>> q.connect()
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

    def wait(self, wait_time=0):
        """
        Returns a :class:`~retask.task.Task` object from the queue. Returns ``False`` if it timeouts.

        :arg wait_time: Time in seconds to wait, default is infinite.

        :return: :class:`~retask.task.Task` object from the queue or False if it timeouts.

        .. doctest::

           >>> from retask.queue import Queue
           >>> q = Queue('test')
           >>> q.connect()
           True
           >>> task = q.wait()
           >>> print task.data
           {u'name': u'kushal'}

        .. note::

            This is a blocking call, you can specity wait_time argument for timeout.

        """
        if not self.connected:
            raise ConnectionError('Queue is not connected')

        data = self.rdb.brpop(self._name, wait_time)
        if data:
            task = Task()
            task.__dict__ = json.loads(data[1])
            return task
        else:
            return False

    def dequeue(self):
        """
        Returns a :class:`~retask.task.Task` object from the queue. Returns ``None`` if the
        queue is empty.

        :return: :class:`~retask.task.Task` object from the queue

        If the queue is not connected then it will raise
        :class:`retask.ConnectionError`

        .. doctest::

           >>> from retask.queue import Queue
           >>> q = Queue('test')
           >>> q.connect()
           True
           >>> t = q.dequeue()
           >>> print t.data
           {u'name': u'kushal'}

        """
        if not self.connected:
            raise ConnectionError('Queue is not connected')

        if self.rdb.llen(self._name) == 0:
            return None

        data = self.rdb.rpop(self._name)
        task = Task()
        task.__dict__ = json.loads(data)
        return task

    def enqueue(self, task):
        """
        Enqueues the given :class:`~retask.task.Task` object to the queue and returns
        a :class:`~retask.queue.Job` object.

        :arg task: ::class:`~retask.task.Task` object

        :return: :class:`~retask.queue.Job` object

        If the queue is not connected then it will raise
        :class:`retask.ConnectionError`.

        .. doctest::

           >>> from retask.queue import Queue
           >>> q = Queue('test')
           >>> q.connect()
           True
           >>> from retask.task import Task
           >>> task = Task({'name':'kushal'})
           >>> job = q.enqueue(task)

        """
        if not self.connected:
            raise ConnectionError('Queue is not connected')

        try:
            #We can set the value to the queue
            job = Job(self.rdb)
            task.urn = job.urn
            text = json.dumps(task.__dict__)
            self.rdb.lpush(self._name, text)
        except Exception, err:
            return False
        return job

    def send(self, task, result, expire=60):
        """
        Sends the result back to the producer. This should be called if only you
        want to return the result in async manner.

        :arg task: ::class:`~retask.task.Task` object
        :arg result: Result data to be send back. Should be in JSON serializable.
        :arg expire: Time in seconds after the key expires. Default is 60 seconds.
        """
        self.rdb.lpush(task.urn, json.dumps(result))
        self.rdb.expire(task.urn, expire)

    def __repr__(self):
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.name)

    def find(self, obj):
        """Retruns the index of the given object in the queue, it might be string
        which will be searched inside each task.

        :arg obj: object we are looking

        :return: -1 if the object is not found or else the location of the task
        """
        if not self.connected:
            raise ConnectionError('Queue is not connected')

        data = self.rdb.lrange(self._name, 0, -1)
        for i, datum in enumerate(data):
            if datum.find(str(obj)) != -1:
                return i
        return -1


class Job(object):
    """
    Job object containing the result from the workers.

    :arg rdb: The underlying redis connection.
    """
    def __init__(self, rdb):
        self.rdb = rdb
        self.urn = uuid.uuid4().urn
        self.__result = None

    @property
    def result(self):
        """
        Returns the result from the worker for this job. This is used to pass
        result in async way.
        """
        if self.__result:
            return self.__result
        data = self.rdb.rpop(self.urn)
        if data:
            self.rdb.delete(self.urn)
            data = json.loads(data)
            self.__result = data
            return data
        else:
            return None

    def wait(self, wait_time=0):
        """
        Blocking call to check if the worker returns the result. One can use
        job.result after this call returns ``True``.

        :arg wait_time: Time in seconds to wait, default is infinite.

        :return: `True` or `False`.

        .. note::

            This is a blocking call, you can specity wait_time argument for timeout.

        """
        if self.__result:
            return True
        data = self.rdb.brpop(self.urn, wait_time)
        if data:
            self.rdb.delete(self.urn)
            data = json.loads(data[1])
            self.__result = data
            return True
        else:
            return False
