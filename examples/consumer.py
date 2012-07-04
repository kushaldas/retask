from retask.task import Task
from retask.queue import Queue
queue = Queue('example')
queue.connect()
while queue.length != 0:
    task = queue.dequeue()
    print task.data

