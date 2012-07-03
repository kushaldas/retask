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
__version__ = '0.1'

"""
retask Queue implementation

"""
import redis
import json
from task import Task



class Queue:
    """
    Returns the ``Queue`` object with the given name. If the user
    passes optional config dictionary with details for Redis
    server, it will connect to that instance. By default it connects
    to the localhost.
    
    """
    def __init__(self, name, config = {}):
        self.name = name
        if not config:
            self.config = {'host':'localhost', 'port':6379, 'db':0,\
                           'password':None}
        else:
            self.config = config
        self.rdb = None
        self.connected = False
        
    @property   
    def length(self):
        """
        Gives the length of the queue. Returns ``None`` if the queue is not
        connected.
        
        """
        if not self.connected:
            return None
        
        return self.rdb.llen(self.name)
    
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
        self.rdb = redis.Redis(config['host'], config['port'], config['db'], 
                              config['password'])
        try:
            info = self.rdb.info()
            self.connected = True
        except redis.ConnectionError:
            return False
        
        return True
          
    def dequeue(self):
        """
        Returns a :class:`Task` object from the queue. Returns ``None`` if the
        queue is empty.
  
        :return: :class:`Task` object from the queue
        
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
            return None
        
        if self.rdb.llen(self.name) == 0:
            return None
        
        data = self.rdb.rpop(self.name)
        task = Task(data, True)
        return task
    
    def enqueue(self, task):
        """
        Enqueues the given :class:`Task` object to the queue and returns
        a tuple. Value in index 0 is ``Boolean`` explaining the enqueue
        operation is a success or not. Value at index 1 is string with 
        error/success message (if any).
        
        :arg task: :class:`Task` object
        
        :return: Tuple with ``Boolean`` value and ``string`` message. 
  
        .. doctest::
  
           >>> from retask.queue import Queue
           >>> q = Queue('test')
           >>> q.connect()
           True
           >>> from retask.task import Task
           >>> task = Task({'name':'kushal'})
           >>> q.enqueue(task)
           (True, 'Pushed')
        
        """
        if not self.connected:
            return False, 'Not connected'
        
        if not task.data:
            return False, 'No data'
        try:
            #We can set the value to the queue
            self.rdb.lpush(self.name, task.rawdata)
        except Exception, err:
            return False, str(err)
        return True, 'Pushed'