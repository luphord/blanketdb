=====
Usage
=====

Command line
------------

To use BlanketDB as a standalone database (and communicate over HTTP), enter the following command:

.. code-block:: console

    $ python3 -m blanketdb -i localhost -p 8080 -f /path/to/db.sqlite

BlanketDB will now serve its web interface at http://localhost:8080.
You can open this page in your browser to check if everything works.

The following command line options are available:

.. code-block:: console

    usage: blanketdb.py [-h] [-i INTERFACE] [-p PORT] [-f FILE]

    Start a BlanketDB instance using wsgiref.simple_server.

    optional arguments:
    -h, --help            show this help message and exit
    -i INTERFACE, --interface INTERFACE
                            Interface to listen on
    -p PORT, --port PORT  Port to listen on
    -f FILE, --file FILE  Database file to use


Python
------

To use BlanketDB in a project, enter the following Python code:

.. code-block:: python

    from blanketdb import BlanketDB
    db = BlanketDB('/path/to/db.sqlite')

    # you can now use db using its Python API
    db.store_dict(x='test')['id']
    for entry in db:
        print(entry)

    # db is alse a wsgi conforming callable
    # you can use it e.g. with the wsgi reference implementation
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8080, db)
    httpd.serve_forever()

You may want to check the `Python API of BlanketDB`__.

__ blanketdb.html