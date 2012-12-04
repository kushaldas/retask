from retask.task import Task
from retask.queue import Queue
queue = Queue('example')
info1 = {'user': 'Fedora planet', 'url': 'http://planet.fedoraproject.org'}
task1 = Task(info1)
queue.connect()
job = queue.enqueue(task1)
job.wait()
print job.result
