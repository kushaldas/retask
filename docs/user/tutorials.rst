.. _tutorials:

Tutorials
=========

This section of the document we have in depth examples of various use cases.

Async data transfer between producer and worker
------------------------------------------------
In many real life scenarios we need to send the result back from the worker instances 
to the producer. The following code examples shows how to achieve that.

async_producer.py
++++++++++++++++++

::

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


Here queue.enqueue method returns a :class:`~retask.queue.Job` object. We can access job.result
to see returned result from a worker. If there is no result yet came back from the worker, it will
print `None`. If you don't need any returned data from the worker you can safely ignore the job object.

async_consumer.py
++++++++++++++++++

::

    from retask import Task
    from retask import Queue
    import time
    queue = Queue('example')
    queue.connect()
    task = queue.wait()
    print(task.data)
    time.sleep(15)
    queue.send(task, "We received your information dear %s" % task.data['user'])


In the above example we see two newly introduced methods :class:`~retask.queue.Queue`.
:func:`~retask.queue.Queue.wait` is a blocking call to wait for a new task in the queue. This is
the preferred method over polling using :func:`~retask.queue.Queue.dequeue`.
To send the result back workers will use :func:`~retask.queue.Queue.send` method, which takes an optional argument
`wait_time` to specify timeout value in seconds.

Synchronous / blocking wait for the result
-------------------------------------------

:: 

    from retask import Task
    from retask import Queue
    queue = Queue('example')
    info1 = {'user': 'Fedora planet', 'url': 'http://planet.fedoraproject.org'}
    task1 = Task(info1)
    queue.connect()
    job = queue.enqueue(task1)
    job.wait()
    print(job.result)

In this example we are using :func:`~retask.queue.Job.wait` function to do a blocking
synchronous call to the worker.
