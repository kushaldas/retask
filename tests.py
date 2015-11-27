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
        self.assertEqual(results[0], 'retaskqueue-lambda')

    def tearDown(self):
        rdb = redis.Redis()
        rdb.delete('retaskqueue-lambda')


class PQSetTest(unittest.TestCase):
    """
    Sets a task in the Queue

    """
    def setUp(self):
        self.queue = PriorityQueue('set_test_queue')
        self.queue.connect()

    def runTest(self):
        t = Task({'name':'josep'})
        self.assertTrue(self.queue.enqueue(t, 100))

    def tearDown(self):
        self.queue.rdb.delete(self.queue._name)


class PQGetTest(unittest.TestCase):
    """
    Sets a task in the Queue

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



if __name__ == '__main__':
    unittest.main()


