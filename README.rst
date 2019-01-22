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




BlanketDB is a very simple database written in Python based on SQLite.
It is intended for small IoT projects where you need a quick way to
collect and store data from sensors and other devices.
You communicate to BlanketDB using HTTP GET / POST / DELETE requests.
Request and response bodies are usually JSON, but you can also POST
HTML forms directly to BlanketDB.
There is no schema in the database, you simply store objects in buckets.



BlanketDB is free software provided under a MIT license.
Documentation is available https://blanketdb.readthedocs.io.


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

Credits
-------

Main author and project maintainer is luphord_.

This package was prepared with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _luphord: https://github.com/luphord
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
