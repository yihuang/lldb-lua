INSTALL
=======

.. code-block::

    $ cat >> ~/.lldbinit
    command script import ~/src/lldb-lua/lldb_lua.py

USE
===

.. code-block::
    

    $ lldb ./main
    (lldb) ... breaked
    (lldb) luatrace     # auto find lua_State* in stack named "L".
    (lldb) luatrace 0x.......  # use address as lua_State*.
    (lldb)
       ...
       lua stack trace
       ...
