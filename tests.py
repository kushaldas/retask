# -*- coding: utf-8 -*-


import threading
import unittest

import redis
from mock import patch
from retask import Task
from retask import Queue
from retask import PriorityQueue


class ConnectTest(unittest.TestCase):
    """
    Test the connect method
    """
    def runTest(self):
        queue = Queue('testqueue')
        self.assertTrue(queue.connect())


class LengthTest(unittest.TestCase):
    """
    Tests the length method of the Queue

    """
    @patch('redis.StrictRedis')
    def runTest(self, mock_redis):
        m = mock_redis.return_value
        m.llen.return_value = 2
        queue = Queue('testqueue')
        queue.connect()
        self.assertEqual(queue.length, 2)


class SetTest(unittest.TestCase):
    """
    Sets a task in the Queue

    """
    def runTest(self):
        queue = Queue('testqueue')
        queue.connect()
        t = Task({'name': 'kushal'})
        self.assertTrue(queue.enqueue(t))

    def tearDown(self):
        rdb = redis.Redis()
        rdb.delete('retaskqueue-testqueue')


class GetTest(unittest.TestCase):
    """
    Gets a task in the Queue

    """
    def setUp(self):
        queue = Queue('testqueue')
        queue.connect()
        t = Task({'name': 'kushal'})
        queue.enqueue(t)

    def runTest(self):
        queue = Queue('testqueue')
        queue.connect()
        task = queue.dequeue()
        self.assertEqual(task.data['name'], 'kushal')


class GetQueueNamesTest(unittest.TestCase):
    """
    Gets a task in the Queue

    """
    def setUp(self):
        queue = Queue('lambda')
        queue.connect()
        t = Task({'name': 'kushal'})
        queue.enqueue(t)

    def runTest(self):
        queue = Queue('lambda')
        queue.connect()
        results = queue.names()
        self.assertEqual(results[0], 'retaskqueue-lambda')

    def tearDown(self):
        rdb = redis.Redis()
        rdb.delete('retaskqueue-lambda')


class PQEnqueueTest(unittest.TestCase):
    """
    Sets a task in the Queue

    """
    def setUp(self):
        self.queue = PriorityQueue('set_test_queue')
        self.queue.connect()

    def runTest(self):
        t = Task({'name': 'josep'})
        self.assertTrue(self.queue.enqueue(t, 100))

    def tearDown(self):
        self.queue.rdb.delete(self.queue._name)


class PQDequeueOrderTest(unittest.TestCase):
    """
    Gets tasks from the Queue

    """
    def setUp(self):
        self.queue = PriorityQueue('get_test_queue')
        self.queue.connect()

        self.queue.enqueue(Task({'index': 1}), 50)
        self.queue.enqueue(Task({'index': 3}), 25)
        self.queue.enqueue(Task({'index': 2}), 40)
        self.queue.enqueue(Task({'index': 0}), 100)

    def runTest(self):
        for i in xrange(4):
            t = self.queue.dequeue()
            self.assertEqual(t.data['index'], i)

    def tearDown(self):
        self.queue.rdb.delete(self.queue._name)


class PQReverseDequeueOrderTest(unittest.TestCase):
    """
    Gets tasks from the Queue in reverse order

    """
    def setUp(self):
        self.queue = PriorityQueue('get_reverse_test_queue', reverse_order=True)
        self.queue.connect()

        self.queue.enqueue(Task({'index': 2}), 50)
        self.queue.enqueue(Task({'index': 0}), 25)
        self.queue.enqueue(Task({'index': 1}), 40)
        self.queue.enqueue(Task({'index': 3}), 100)

    def runTest(self):
        for i in xrange(4):
            t = self.queue.dequeue()
            self.assertEqual(t.data['index'], i)

    def tearDown(self):
        self.queue.rdb.delete(self.queue._name)


class PQWaitTimeoutTest(unittest.TestCase):
    """
    Tries to wait for a task until the operation runs out of time.

    """
    def setUp(self):
        self.queue = PriorityQueue('wait_timeout_test_queue')
        self.timer = threading.Timer(1, self.addTask)
        self.queue.connect()

    def runTest(self):
        t = self.queue.wait(wait_time=1)
        self.assertFalse(t)

        self.timer.start()
        t = self.queue.wait(wait_time=5)
        self.assertEqual(t.data['text'], 'timeout ...')

    def addTask(self):
        self.queue.enqueue(Task({'text': 'timeout ...'}), 10)

    def tearDown(self):
        self.queue.rdb.delete(self.queue._name)


class PQWaitTest(unittest.TestCase):
    """
    Waits for a task until one is available.
    """
    def setUp(self):
        self.queue = PriorityQueue('wait_no_timeout_test_queue')
        self.timer = threading.Timer(3, self.addTask)
        self.queue.connect()

    def runTest(self):
        self.timer.start()

        t = self.queue.wait()
        self.assertEqual(t.data['text'], 'waiting ...')

    def addTask(self):
        self.queue.enqueue(Task({'text': 'waiting ...'}), 10)

    def tearDown(self):
        self.queue.rdb.delete(self.queue._name)


class PQWaitTestMultipleConsumers(unittest.TestCase):
    """
    Two threads infinitely waiting for a task.

    """
    def setUp(self):
        self.queue = PriorityQueue('wait_nto_consumers_test_queue')
        self.timer1 = threading.Timer(1.5, self.addTask1)
        self.timer2 = threading.Timer(2.5, self.addTask2)
        self.expected_msgs = frozenset(['waiting1', 'waiting2'])
        self.queue.connect()

    def runTest(self):
        self.timer1.start()
        self.timer2.start()

        t1 = threading.Thread(target=self.waitTask)
        t2 = threading.Thread(target=self.waitTask)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def addTask1(self):
        self.queue.enqueue(Task({'text': 'waiting1'}), 10)

    def addTask2(self):
        self.queue.enqueue(Task({'text': 'waiting2'}), 20)

    def waitTask(self):
        t = self.queue.wait()
        self.assertTrue(t.data['text'] in self.expected_msgs)

    def tearDown(self):
        self.queue.rdb.delete(self.queue._name)


if __name__ == '__main__':
    unittest.main()
