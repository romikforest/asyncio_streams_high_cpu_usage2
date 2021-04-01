This is an example of high cpu usage using asyncio streams and pool of multiple connections

There is a simple server that serve socket connections and a client (that also a server for http requests)
Client recieves http requests GET /, sends socket request to the server, recieves a fictive response and answers that data has been recieved to the http client.
As http client I have locust here.
Http is served by starlette + uvicorn
I used also this library  https://github.com/fellowapp/asyncio-connection-pool to create a connection pool.
This example uses the original non patched library.

As a result I have a high cpu usage on cpython 3.8 - 3.9.
The signal handler _signalhandler_noop (unix_events.py) is executed continously.
It affects at least mac and debian.

Way to install and reproduce:

On mac:
brew install qcachegrind

pip install -r requiremnts.txt

In different terminals tabs:

python server.py

python -m cProfile -o client.cprof client.py

locust

To locust example parameters are:
Number of users to simulate: 50
Spawn rate: 1
Host: http://127.0.0.1:8000

After users reach 50 and some exposition:

Ctrl+C to stop the locust, client and server.

To view profile results:
pyprof2calltree -k -i client.cprof
