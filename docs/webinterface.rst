=============
Web interface
=============

This section documents the Web interface (HTTP API) of BlanketDB.
For simplicity we assume that BlanketDB is served at
http://localhost:8080.

Create entries
--------------

To create an entry in the default bucket perform this request:

.. code-block:: console

    POST http://localhost:8080/

The body of the POST request may either be an arbitrary JSON object, e.g.:

.. code-block:: json

    {
        "a": 1.23,
        "test": "somedata"
    }

or URL-encoded form content (as is created by standard HTML form submission), e.g.:

.. code-block:: console

    a=1.23&test=somedata

In both cases, BlanketDB will answer with a JSON object like:

.. code-block:: json

    {
        "id": 3,
        "bucket": "default",
        "timestamp": "2019-01-23T17:11:41.168836",
        "data": {
            "a": 1.23,
            "test": "somedata"
        }
    }

If you want to store to a bucket named `mybucket`, post to this URL:

.. code-block:: console

    POST http://localhost:8080/mybucket

Query database
--------------

TODO

Delete entries
--------------

TODO