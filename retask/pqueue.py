#Copyright (C) 2015, Josep Pon Farreny <jponfarreny@gmail.com>

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

__author__ = 'Josep Pon Farreny <jponfarreny@gmail.com>'
__copyright__ = 'Copyright (c) 2015 Josep Pon Farreny'
__license__ = 'MIT'
__status__ = 'Production/Stable'
__version__ = '1.0'

"""
retask PriorityQueue implementation

"""

import json
import redis
import six
import logging

import exceptions
import queue
import task

# -------------- #
# Event messages #

_PRIORITY_QUEUE_READY_MSG = "pq-ready"


# ------------- #
# PriorityQueue #

# TODO Add a parameter to retrieve tasks or tasks + priority


class PriorityQueue(queue.Queue):
    """
    Returns the ``PriorityQueue`` object with the given name. If the user
    passes optional config dictionary with details for Redis server, it
    will connect to that instance. By default it connects to the localhost.

    """

    def __init__(self, name, config=None, reverse_order=False):
        super(PriorityQueue, self).__init__(name, config)
        self._name = 'retask-priorityqueue-' + name        # override Queue name
        self._wc_name = 'retask-priorityqueue-wc-' + name  # wait channel name
        self._reverse_order = reverse_order

    @property
    def length(self):
        if not self.connected:
            raise exceptions.ConnectionError('PriorityQueue is not connected')

        try:
            return self.rdb.zcard(self._name)
        except redis.exceptions.ConnectionError as e:
            raise exceptions.ConnectionError(str(e))

    def wait(self, wait_time=0):
        """
        Returns a :class:`~rtask.task.Task` object from the queue.
        Returns ``False`` if it timeouts.

        :arg wait_time: Time in seconds to wait, default is infinite.

        :return: :class:`~retask.task.Task` object from the queue or
                 False if it timeouts.

        .. doctest::

           >>> from retask import Queue
           >>> q = Queue('test')
           >>> q.connect()
           True
           >>> task = q.wait()
           >>> print task.data
           {u'name': u'kushal'}

        .. note::

            This is a blocking call, you can specity wait_time argument for timeout.

        """
        # TODO add timeout support
        if not self.connected:
            raise exceptions.ConnectionError('PriorityQueue is not connected')

        ps = self._rdb.pubsub(ignore_subscribe_messages=True)
        ps.subscribe(self._wc_name)
        ps_listener = ps.listen()

        data = self._try_pop()
        while data is None:
            msg = next(ps_listener)
            if msg["data"] == _PRIORITY_QUEUE_READY_MSG:
                data = self._try_pop()

        ps.unsubscribe(self._wc_name)
        ps.close()

        t = task.Task()
        t.__dict__ = json.loads(data)

    def dequeue(self):
        """
        Returns a :class:`~retask.task.Task` object from the queue. Returns ``None`` if the
        queue is empty.

        :return: :class:`~retask.task.Task` object from the queue

        If the queue is not connected then it will raise
        :class:`retask.ConnectionError`
        """
        if not self.connected:
            raise exceptions.ConnectionError('PriorityQueue is not connected')

        data = self._try_pop()

        if data:
            if isinstance(data, six.binary_type):
                data = six.text_type(data, 'utf-8', errors='replace')
            t = task.Task()
            t.__dict__ = json.loads(data)
            return t

        return None

    def enqueue(self, task, priority):
        """
        Enqueues the given :class:`~retask.task.Task` object to the queue and returns
        a :class:`~retask.queue.Job` object.

        :arg task: ::class:`~retask.task.Task` object
        :arg priority: 

        :return: :class:`~retask.queue.Job` object

        If the queue is not connected then it will raise
        :class:`retask.ConnectionError`.

        """
        if not self.connected:
            raise exceptions.ConnectionError('PriorityQueue is not connected')

        try:
            job = queue.Job(self.rdb)
            task.urn = job.urn
            text = json.dumps(task.__dict__)
            self.rdb.zadd(self._name, priority, text)

            self.rdb.publish(self._wc_name, _PRIORITY_QUEUE_READY_MSG)
            return job
        except redis.ConnectionError as e:
            raise exceptions.ConnectionError(str(e))

    def find(self, obj):
        """Returns the index of the given object in the queue, it might be string
        which will be searched inside each task.

        :arg obj: object we are looking

        :return: -1 if the object is not found or else the location of the task
        """
        if not self.connected:
            raise ConnectionError('Queue is not connected')

        data = self.rdb.zrange(self._name, 0, -1)
        for i, datum in enumerate(data):
            if datum.find(str(obj)) != -1:
                return i
        return -1

    def _try_pop(self):
        # pyredis 2.7.2 transactions do not support 'value_from_callable'
        # A callable class is used as a workarround to this issue
        class _Transaction(object):

            def __init__(self, name, reverse_order):
                self.name = name
                self.reverse_order = reverse_order
                self.result = None

            def __call__(self, pipe):  # this is the transaction function
                range_func = pipe.zrange if self.reverse_order else pipe.zrevrange
                elements = range_func(self.name, 0, 0, withscores=False)
                if elements:
                    pipe.multi()
                    pipe.zrem(self.name, *elements)
                    self.result = elements[0]

        transaction = _Transaction(self._name, self._reverse_order)
        self.rdb.transaction(transaction, self._name,
                             value_from_callable=True)
        return transaction.result
