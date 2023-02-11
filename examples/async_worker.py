from retask import Queue
import time
queue = Queue('example')
queue.connect()
task = queue.wait()
print(task.data)
time.sleep(15)
queue.send(task, "We received your information dear %s" % task.data['user'])
