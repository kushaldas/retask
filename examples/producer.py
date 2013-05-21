from retask import Task
from retask import Queue
queue = Queue('example')
info1 = {'user':'kushal', 'url':'http://kushaldas.in'}
info2 = {'user':'fedora planet', 'url':'http://planet.fedoraproject.org'}
task1 = Task(info1)
task2 = Task(info2)
queue.connect()
queue.enqueue(task1)
queue.enqueue(task2)

