Running and embedding
=====================

Only two files are required
---------------------------
LCODE 3D is a single-file module and you only need two files to execute it:
``lcode.py`` and ``config.py``.

Installing LCODE into ``PYTHONPATH`` with the likes of ``pip install .`` is possible,
but is not officially supported.


Configuration with config.py
----------------------------
The simplest way to configure LCODE 3D is
to place a file ``config.py`` into the current working directory.
An example is provided as ``config_example.py``.

The file gets imported by the standard Python importing mechanism,
the resulting module is passed around internally as ``config``.

One can use all the features of Python inside the configuration file,
from arithmetic expressions and functions to other modules and metaprogramming.

For executing, try
``python3 lcode.py``, ``python lcode.py`` or ``./lcode.py``.


Configuration with executable config
------------------------------------
The second way is to create a config file,
make sure that it ends with

.. code-block:: python

  if __name__ == '__main__':
      import sys, lcode; lcode.main(sys.modules[__name__])

and execute the configuration file directly.

``lcode.py`` should be either located inside the working directory
or installed to ``PYTHONPATH``.

This way may be preferrable if you want to manage several configuration files.

For executing, try
``python3 some_config.py``, ``python some_config.py`` or ``./some_config.py``.


Configuration with a Python object
----------------------------------
The third way is to create a Python object with all the required attributes
and to pass it to
:func:`lcode.main`, :func:`lcode.init` + :func:`lcode.step`,
or even smaller bits and pieces from your code.

This way may come in handy if you are calling LCODE 3D from other Python programs.
