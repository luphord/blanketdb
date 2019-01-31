=========
BlanketDB
=========


.. image:: https://img.shields.io/pypi/v/blanketdb.svg
        :target: https://pypi.python.org/pypi/blanketdb

.. image:: https://img.shields.io/travis/luphord/blanketdb.svg
        :target: https://travis-ci.org/luphord/blanketdb

.. image:: https://readthedocs.org/projects/blanketdb/badge/?version=latest
        :target: https://blanketdb.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


BlanketDB_ is a very simple database written in Python based on SQLite.
It is intended for small IoT projects where you need a quick way to
collect and store data from sensors and other devices.
You communicate to BlanketDB using HTTP GET / POST / DELETE requests.
Request and response bodies are usually JSON, but you can also POST
HTML forms directly to BlanketDB.
There is no schema in the database, you simply store objects in buckets.

BlanketDB is free software provided under a MIT license.
Documentation is available at https://blanketdb.readthedocs.io.

Why is it called BlanketDB? Well, a blanket_ is simple, lightweight, portable
and keeps you warm. But if you really want to relax, you'll need a couch_.

.. _BlanketDB: https://github.com/luphord/blanketdb
.. _blanket: https://github.com/luphord/blanketdb
.. _couch: http://couchdb.apache.org/


Features
--------

* GET / POST / DELETE requests to communicate with BlanketDB
* JSON requests / responses
* HTML forms can POST directly to BlanketDB
* Data stored in buckets
* Schemaless
* Query using various parameters to a HTTP GET request
* Data is stored in a single file on the file system which is a SQLite database
* BlanketDB is a single Python file without any dependencies besides the standard library
* No sequrity whatsoever; BlanketDB is completely open to readers and writers (use with care!)

Quickstart
----------

To install BlanketDB, you'll need a Python (>=3.4) installation with pip:

.. code-block:: console

    $ pip install blanketdb

To use BlanketDB as a standalone database (and communicate over HTTP), enter the following command:

.. code-block:: console

    $ python3 -m blanketdb -i localhost -p 8080 -f /path/to/db.sqlite

BlanketDB will now serve its web interface at http://localhost:8080.
You can open this page in your browser to check if everything works.

To use BlanketDB in a Python project, enter the following code:

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

Detailed documentation is available at https://blanketdb.readthedocs.io.

Credits
-------

Main author and project maintainer is luphord_.

This package was prepared with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _luphord: https://github.com/luphord
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
