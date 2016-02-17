.. _quickstart:

Quickstart
==========

For this example to work you should have your redis instance
up and running.

producer.py
-----------
This code puts new task in the queue. We will have a dictionary as
the information in this example.

::

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


consumer.py
-----------
This code gets the tasks from the queue. Based on the actual requirement, the
client will work on the information it received as the task. For now we will
just print the data.

::

    from retask import Task
    from retask import Queue
    queue = Queue('example')
    queue.connect()
    while queue.length != 0:
        task = queue.dequeue()
        if task:
            print(task.data)

