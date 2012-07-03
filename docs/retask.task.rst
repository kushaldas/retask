:mod:`retask.task`
=======================
This module conatins generic task class, which can be used to create
any kind of given task with serializable python objects as data.



.. class:: Task(data=None, raw=False)

   Returns a new Task object, the information for the task is passed through
   argument ``data``.

   .. data:: data

      Returns the python object containing information for the current task.


   .. data:: rawdata

      Returns the string representation of the actual python objects for the task

      .. note:: 

         This should not be used directly by the users. This is for internal use
         only.
