=======================
k2ksm: The QUIT Command
=======================

Honestly, I'm not sure why I made this document!  I probably just made it to be complete.

The QUIT series of commands has one "sub-command"::

	QUIT

The QUIT command tells the server that the client would like to disconnect.  The server should respond with an OK, followed by a BYE.  The server should then close the connection.