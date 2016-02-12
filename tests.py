import unittest
import redis
from mock import patch
from retask import Task
from retask import Queue


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
    @patch('redis.Redis')
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
        t = Task({'name':'kushal'})
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
        t = Task({'name':'kushal'})
        queue.enqueue(t)


    def runTest(self):
        queue = Queue('testqueue')
        queue.connect()
        task = queue.dequeue()
        i = task.data
        self.assertEqual(task.data['name'], 'kushal')

class GetQueueNamesTest(unittest.TestCase):
    """
    Gets a task in the Queue

    """
    def setUp(self):
        queue = Queue('lambda')
        queue.connect()
        t = Task({'name':'kushal'})
        queue.enqueue(t)

    def runTest(self):
        queue = Queue('lambda')
        queue.connect()
        results = queue.names()
        self.assertEqual(results[0], 'lambda')

    def tearDown(self):
        rdb = redis.Redis()
        rdb.delete('retaskqueue-lambda')

if __name__ == '__main__':
    unittest.main()


