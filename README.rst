.. image:: https://travis-ci.org/akkornel/k2ksm.svg?branch=master
    :target: https://travis-ci.org/akkornel/k2ksm
.. image:: https://coveralls.io/repos/akkornel/k2ksm/badge.png?branch=master
  :target: https://coveralls.io/r/akkornel/k2ksm?branch=master

===============================================
k2ksm: A key storage and authentication system.
===============================================

**k2ksm** is a suite of components and modules for encryption key storage, and for authentication.  k2ksm is used by clients to authenticate, and to manage keys.  k2ksm tries to reduce the amount of work that the client has to do in order to manage keys and authentication.

k2ksm currently has support for the following key types:

- AES keys (128- and 256-bit)

k2ksm currently has support for the following types of authentication:

- HOTP (6- or 8-digit one-time passwords, based on an AES- key and a counter)
- TOTP (6- or 8-digit one-time passwords, based on an AES- key and the current time)
- YubiOTP (one-time passwords based on an AES- key, multiple counters, and the current time)

k2ksm has two components:

- The *public-facing component* accepts connections from the outside, communicating with clients, and passing data to the internal component.
- The *internal component* runs on a server and doesn't talk to anyone, except for the external component.  All of the crypto stuff happens here.

The public-facing component is designed to accept connections over SSH.  It may also be run locally for debugging and testing.

Communication between the client and the server uses a custom protocol.  See docs/protocol.rst for more information.  For more information about the steps taken to keep private information safe, see docs/security.rst.

