#################
API Documentation
#################

Partify exposes an HTTP API that allows third-party software to interact with a Partify installation. This is useful for developing clients and
services that interact with Partify.

.. note:: Not all elements of Partify have been API'd yet. Full API completion is scheduled for the release of 0.5. See https://github.com/fxh32/partify/issues/88 for more information

.. warning:: The API has no versioning right now, and is therefore subject to change. Until versioning is implemented developers should be aware that endpoints may shift out from under them.


Usage
-----

All requests should be made over HTTP. Responses returned by API endpoints are all formatted as `JSON <http://json.org>`_ strings. Responses are returned as standard HTTP responses. If the
HTTP status code is OK, the response will typically contain a ``status`` member in the root of the response, which indicates the status of the request. This can be either ``ok`` or ``error``. 
If ``status`` is ``error`` then a ``message`` field will also exist in the root of the response describing the error that occurred. If ``status`` is OK, the rest of the response is dependent
on the endpoint returning the response.

Concepts
--------

User queue vs global queue etc.
   

API Reference
-------------

.. toctree::
   :maxdepth: 2

   player
   queue
   search
   vote
   history
   statistics
   user