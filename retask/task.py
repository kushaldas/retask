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

__author__ = 'Kushal Das <kushaldas@gmail.com>'
__copyright__ = 'Copyright (c) 2012-2023 Kushal Das'
__license__ = 'MIT'
__status__ = 'Production/Stable'
__version__ = '1.1.0'

"""
Task Class
"""
import json

from typing import Optional, Any

class Task():
    """
    Returns a new Task object, the information for the task is passed through
    argument ``data``

    :kwarg data: Python object which contains information for the task. Should be serializable through ``JSON``.
    :kwarg raw: If we are receiving raw JSON encoded data.
    :kwarg urn: If we are supping the random URN value as str.

    """

    def __init__(self, data: Optional[object]=None, raw=False, urn=Optional[str]):
        self._data: str = ""
        self.urn: str = ""
        if not raw and data:
            self._data = json.dumps(data)
        else:
            if isinstance(data, str):
                self._data = data
        if isinstance(urn, str):
            self.urn = urn

    @property
    def data(self) -> Any:
        """
        The python object containing information for the current task

        """
        return json.loads(self._data)

    @property
    def rawdata(self) -> str: 
        """
        The string representation of the actual python objects for the task

        .. note::
            This should not be used directly by the users. This is for internal use
            only.

        """
        return self._data

    def __repr__(self) -> str:
            return '%s(%s)' % (self.__class__.__name__, repr(self.data))
