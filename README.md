MDP - the Majordomo Protocol
============================

# RPC-MDP

This is an extension to the MDP implementation of Guido Goldstein.
Now you can use this MDP (reliable ROUTER-DEALER pattern) for RPC (Remote Procedure Calls).

Please check out:
* rpc.py
* mybroker.py
* worker1.py
* worker2.py
* myclient.py

in ./mdp

And you will immediately know how this works. Basically there is now another module called rpc.py which you can import to your Server and Client modules.

For the "Server" part please check out worker1.py or worker2.py
For the "Client" part please check out myclient.py (first cli argument is the worker_id you want to talk to)

Imagine a "Server" (like worker1.py) has a class called Foo() with a method named hello(). Then you can connect with your client and call "myclient.hello()" and the server will respond with its method.


### Original Description of maintainer Guido Golstein
An implementation in Python using pyzmq.

For the specification of see
<center>
<a href="http://rfc.zeromq.org/spec:7">MDP - the Majordomo Protocol<a/>
</center>

The implementation will make use of the more advanced parts of the
pyzmq bindings, namely ioloop and streams.

For this reason, most of the code will *not* look like the examples in
the guide. The examples in the guide are more or less direct
translations of the C examples. But pyzmq does offer more than a
shallow wrapper of the C API.


This is an example of how to use pyzmq, not a full blown solution
for those who need one.


Authors
-------
 * Hasan Pekdemir (https://github.com/omani)

 * Guido Goldstein (https://github.com/guidog)

 * Solomon Hykes (https://github.com/shykes)