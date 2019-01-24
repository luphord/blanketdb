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

Retrieve entries
----------------

To retrieve an individual entry using its ID (e.g. 123), use the following request:

.. code-block:: console

    GET http://localhost:8080/_entry/123

BlanketDB will answer with a response similar to the post request above:

.. code-block:: json

    {
        "id": 123,
        "bucket": "default",
        "timestamp": "2019-01-24T06:31:36.328127",
        "data": {
            "a": 1.23,
            "test": "somedata"
        }
    }

If no entry with the given ID exists, BlanketDB will respond with a `404 Not found`
HTTP error code. Note that you do not specify the bucket of the entry in the URL.
IDs are unique across all buckets in BlanketDB.

The response above shows the data stored in entry 123 as well as corresponding
metadata such as `timestamp` (of creation) and `bucket`. In order to make BlanketDB
omit any metadata use

.. code-block:: console

    GET http://localhost:8080/_entry/123?meta=false

which will result in this reponse:

.. code-block:: json

    {
        "a": 1.23,
        "test": "somedata"
    }

Query database
--------------

TODO

Delete entries
--------------

TODO