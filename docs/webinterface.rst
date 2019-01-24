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

BlanketDB allows you to query entries using these filters:

* `bucket`
* `since_id` entries with the given ID (inclusive) or higher
* `before_id` entries with an ID lower than the given one (exclusive)
* `since` entries created at the given time (inclusive) or later
* `before` entries created before the given time (exclusive)

The `bucket` is specified in the URL, the remaining filters are given as query
parameters. `since` and `before` can be specified as timestamps (e.g.
"2019-01-24T06:52:06.181786" or just "2019-01-24") or as multiples of seconds,
minutes or hours (e.g. "2sec", "7s", "3min", "8m", "1hour", "2hours", "3h").

In order to query all entries of bucket `mybucket` of the last two hours, use this request:

.. code-block:: console

    GET http://localhost:8080/mybucket?since=2hours

BlanketDB will respond in this form:

.. code-block:: json

    {
        "bucket_requested": "mybucket",
        "since_id": 0,
        "since": "2019-01-24T04:59:37.925981",
        "before_id": null,
        "before": null,
        "number_of_entries": 2,
        "last_id": 4,
        "limit": null,
        "newest_first": true,
        "entries": [
            {
                "id": 4,
                "bucket": "mybucket",
                "timestamp": "2019-01-24T06:59:30.462450",
                "data": {
                    "b": 1.23,
                    "test": "somedata2"
                }
            },
            {
                "id": 3,
                "bucket": "mybucket",
                "timestamp": "2019-01-24T06:59:23.005946",
                "data": {
                    "a": 1.23,
                    "test": "somedata"
                }
            }
        ]
    }

In the same way as retrieving individual entries you can omit entry metadata using

.. code-block:: console

    GET http://localhost:8080/mybucket?since=2hours&meta=false

which will result in:

.. code-block:: json

    {
        "bucket_requested": "mybucket",
        "since_id": 0,
        "since": "2019-01-24T05:00:02.552377",
        "before_id": null,
        "before": null,
        "number_of_entries": 2,
        "last_id": 4,
        "limit": null,
        "newest_first": true,
        "entries": [
            {
                "b": 1.23,
                "test": "somedata2"
            },
            {
                "a": 1.23,
                "test": "somedata"
            }
        ]
    }

If you want to limit the number of entries retrieved, you can specify the `limit` parameter.
In this context you will likely want to specify whether you are interested
in the oldest or newest entries. To query the latest 3 entries in `mybucket`, use
the following request (without metadata for brevity)

.. code-block:: console

    GET http://localhost:8080/mybucket?meta=false&limit=3&newest_first=true

which will result in something like this:

.. code-block:: json

    {
        "bucket_requested": "mybucket",
        "since_id": 0,
        "since": null,
        "before_id": null,
        "before": null,
        "number_of_entries": 3,
        "last_id": 6,
        "limit": 3,
        "newest_first": true,
        "entries": [
            {
                "b": 1.23,
                "test": "somedata2"
            },
            {
                "b": 1.23,
                "test": "somedata2"
            },
            {
                "b": 1.23,
                "test": "somedata2"
            }
        ]
    }

If `newest_first` is not specified, it will default to `true` (hence the example
above would work without `newest_first`).

In order to paginate entries you can use a combination of `since_id` and `limit`.
For each subsequent request you would read the `last_id` field of the response,
icrement by 1 and then use that number as the new `since_id`.

Delete entries
--------------

You can delete individual entries using the following request (for entry 123):

.. code-block:: console

    DELETE http://localhost:8080/_entry/123

In addition, you can apply the query filters above when deleting entries.
For example, to delete all entries before today you would use the request:

.. code-block:: console

    DELETE http://localhost:8080/?before=today

BlanketDB will respond with the usual query metadata and a field containing
the number of entries deleted:

.. code-block:: json

    {
        "bucket_requested": null,
        "since_id": 0,
        "since": null,
        "before_id": null,
        "before": "2019-01-24",
        "number_of_entries_deleted": 3
    }
