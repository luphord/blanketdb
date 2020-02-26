=======
History
=======

0.4.0 (2020-02-26)
------------------

* Start uwsgi using http protocol by default in DOCKERFILE (s.t. standalone use is possible)
* Overwrite CMD in docker-compose file to communicate via uwsgi protocol between nginx and blanketdb container

0.3.4 (2020-02-26)
------------------

* Support Python 3.8

0.3.3 (2019-12-12)
------------------

* Split tests into Python and HTTP API tests
* Added tests that can be executed against an actual HTTP API of `BlanketDB`

0.3.2 (2019-12-04)
------------------

* Release to trigger build on dockerhub

0.3.1 (2019-03-06)
------------------

* Improved clarity with default values

0.3 (2019-03-06)
----------------

* Type annotations for `BlanketDB`
* Python 3.4 is not supported anymore (as it does not know type annotations)

0.2.2 (2019-01-31)
------------------

* setuptools entrypoint for cli
* quickstart documentation
* added logo

0.2.1 (2019-01-24)
------------------

* fix tag confusion

0.2.0 (2019-01-24)
------------------

* Added CLI for starting `BlanketDB` with `wsgiref.simple_server`
* Tests for `BlanketDB` Web API using `webtest`
* Added documentation for usage and Web API

0.1.0 (2019-01-18)
------------------

* First release on PyPI.
