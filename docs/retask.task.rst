:mod:`retask.task`
=======================
This module conatins generic task class, which can be used to create
any kind of given task with serializable python objects as data.

.. py:class:: retask.Task(data=None, raw=False)

    Returns a new Task object, the information for the task is passed through argument *data*.

   .. py:attribute:: data

        The python object containing information for the current task
