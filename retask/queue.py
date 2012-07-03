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
    Generic Queue on Redis
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
        Returns the length of the queue
        """
        if not self.connected:
            return None
        
        return self.rdb.llen(self.name)
    
    def connect(self):
        """
        Checks the connectivity with the redis server
        
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
        Gets the first task from the Queue
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
        Sets the given task in the queue
    
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