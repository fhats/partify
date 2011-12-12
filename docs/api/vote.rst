******
Voting
******

.. contents::

Getting the User's Vote Status
------------------------------

To find out what a User's vote (if any) on a track is, use the :func:`/vote/status <partify.vote.vote_status>` endpoint. The endpoint will return ``1``, ``-1``,
or ``0`` if the user has voted the track up, down, or has not voted yet (respectively).

.. autofunction:: partify.vote.vote_status
   :noindex:

.. note:: A user cannot vote on a track he or she has queued; therefore, a user also cannot get his or her vote status on a track queued by him or her.

**Example**

::

	GET /vote/status?pqe=5 HTTP/1.1

::

	{
	  "status": "ok",
	  "direction": 1
	}

Voting a Track Up
-----------------

To vote a track up when a selection scheme that supports voting is enabled, send a ``POST`` to :func:`/vote/up <partify.vote.vote_up>` with the ID of the 
:class:`~partify.models.PlayQueueEntry` to vote on.

.. autofunction:: partify.vote.vote_up
   :noindex:

.. note:: A user may not vote on a track her or she has queued.

**Example**

::

	POST /vote/up HTTP/1.1

	pqe: 5

::

	{
	  "status": "ok"
	}


Voting a Track Down
-------------------

To vote a track down when a selection scheme that supports voting is enabled, send a ``POST`` to :func:`/vote/down <partify.vote.vote_down>` with the ID of the 
:class:`~partify.models.PlayQueueEntry` to vote on.

.. autofunction:: partify.vote.vote_down
   :noindex:

.. note:: A user may not vote on a track her or she has queued.

**Example**

::

	POST /vote/down HTTP/1.1

	pqe: 5

::

	{
	  "status": "ok"
	}


Getting the Vote Score for a Track
----------------------------------

The total vote score of a :class:`~partify.models.PlayQueueEntry` or :class:`~partify.models.PlayHistoryEntry` may be retrieved by all users from the 
:func:`/vote/total <partify.vote.vote_total>` endpoint.

.. autofunction:: partify.vote.vote_total
   :noindex:

**Examples**

For a :class:`~partify.models.PlayQueueEntry`

::

	GET /vote/total?pqe=5 HTTP/1.1

::

	{
	  "status": "ok",
	  "total": 6
	}

For a :class:`~partify.models.PlayHistoryEntry`

::

	GET /vote/total?phe=5 HTTP/1.1

::

	{
	  "status": "ok",
	  "total": -4
	}