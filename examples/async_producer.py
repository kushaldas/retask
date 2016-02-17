from retask import Task
from retask import Queue
import time
queue = Queue('example')
info1 = {'user': 'Fedora planet', 'url': 'http://planet.fedoraproject.org'}
task1 = Task(info1)
queue.connect()
job = queue.enqueue(task1)
print(job.result)
time.sleep(30)
print(job.result)
