******
Player
******

.. contents::

.. _api_get_player_status:

Getting Player Status
---------------------

Clients can retrieve Partify player status information by sending a ``GET`` to the endpoint :func:`/player/status/poll <partify.player.status>`. The parameter ``current`` can be used
to save bandwidth and processing by indicating that the client has a recent version of the global and user play queues and that it does not need to be updated. 
``current`` should be set as a float corresponding to a timestamp in seconds of the time the last playlist update was received. If the playlist has been 
updated since ``current``, the global and user play queues will be sent. If ``current`` is omitted the current user and global play queues are sent to the client.

The built-in Partify client hits this endpoint every 3 seconds to maintain synchronization. Updating too frequently may flood the server and cause Partify 
to become unresponsive.

.. autofunction:: partify.player.status
   :noindex:


.. note:: This endpoint does not currently return a status key in the root of the JSON response. This will change in the future.

**Examples**

With ``current`` defined::

	GET /player/status/poll?current=1323664610.545476 HTTP/1.1

::

	{
	  "album": "Codes and Keys", 
	  "repeat": "0", 
	  "consume": "1", 
	  "artist": "Death Cab for Cutie", 
	  "pqe_id": 23, 
	  "random": "0", 
	  "state": "play", 
	  "volume": "100", 
	  "single": "0", 
	  "file": "spotify:track:0b16PJlDwSaBPqM9uyyujg", 
	  "time": "259", 
	  "date": "2011-01-01", 
	  "title": "Monday Morning", 
	  "id": "101", 
	  "response_time": 1323654783.606083
	}

Without ``current``::

	GET /player/status/poll HTTP/1.1

::

	{
	  "user_queue": [
	    {
	      "album": "Codes and Keys", 
	      "username": "fred", 
	      "playback_priority": 0, 
	      "user_id": 1, 
	      "artist": "Death Cab for Cutie", 
	      "spotify_url": "spotify:track:0b16PJlDwSaBPqM9uyyujg", 
	      "length": 258.906, 
	      "mpd_id": 101, 
	      "user_priority": 23, 
	      "date": "2011", 
	      "title": "Monday Morning", 
	      "time_added": "Sun Dec 11 20:02:17 2011", 
	      "id": 23, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Act III: Life And Death", 
	      "username": "fred", 
	      "playback_priority": 1, 
	      "user_id": 1, 
	      "artist": "The Dear Hunter", 
	      "spotify_url": "spotify:track:1mtqSm1apPn7o69P10L9L8", 
	      "length": 301.24, 
	      "mpd_id": 102, 
	      "user_priority": 24, 
	      "date": "2009", 
	      "title": "The Thief", 
	      "time_added": "Sun Dec 11 20:02:47 2011", 
	      "id": 24, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Constellations", 
	      "username": "fred", 
	      "playback_priority": 2, 
	      "user_id": 1, 
	      "artist": "Darwin Deez", 
	      "spotify_url": "spotify:track:3DbEgIX3u7crwCcbOQbcAf", 
	      "length": 187, 
	      "mpd_id": 103, 
	      "user_priority": 25, 
	      "date": "2010", 
	      "title": "The Coma Song", 
	      "time_added": "Sun Dec 11 20:03:39 2011", 
	      "id": 25, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Darwin Deez", 
	      "username": "fred", 
	      "playback_priority": 3, 
	      "user_id": 1, 
	      "artist": "Darwin Deez", 
	      "spotify_url": "spotify:track:2GpgyczUEfniHZdKwvU843", 
	      "length": 186.131, 
	      "mpd_id": 104, 
	      "user_priority": 26, 
	      "date": "2011", 
	      "title": "Bad Day", 
	      "time_added": "Sun Dec 11 20:03:53 2011", 
	      "id": 26, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Feel Good Lost", 
	      "username": "fred", 
	      "playback_priority": 4, 
	      "user_id": 1, 
	      "artist": "Broken Social Scene", 
	      "spotify_url": "spotify:track:6GIV7S7zOxJSxBrNsWaFRZ", 
	      "length": 344.653, 
	      "mpd_id": 105, 
	      "user_priority": 27, 
	      "date": "2004", 
	      "title": "Love And Mathematics", 
	      "time_added": "Sun Dec 11 20:05:19 2011", 
	      "id": 27, 
	      "user": "Fred"
	    }, 
	  ], 
	  "consume": "1", 
	  "pqe_id": 23, 
	  "random": "0", 
	  "elapsed": "44.223", 
	  "volume": "100", 
	  "global_queue": [
	    {
	      "album": "Codes and Keys", 
	      "username": "fred", 
	      "playback_priority": 0, 
	      "user_id": 1, 
	      "artist": "Death Cab for Cutie", 
	      "spotify_url": "spotify:track:0b16PJlDwSaBPqM9uyyujg", 
	      "length": 258.906, 
	      "mpd_id": 101, 
	      "user_priority": 23, 
	      "date": "2011", 
	      "title": "Monday Morning", 
	      "time_added": "Sun Dec 11 20:02:17 2011", 
	      "id": 23, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Act III: Life And Death", 
	      "username": "fred", 
	      "playback_priority": 1, 
	      "user_id": 1, 
	      "artist": "The Dear Hunter", 
	      "spotify_url": "spotify:track:1mtqSm1apPn7o69P10L9L8", 
	      "length": 301.24, 
	      "mpd_id": 102, 
	      "user_priority": 24, 
	      "date": "2009", 
	      "title": "The Thief", 
	      "time_added": "Sun Dec 11 20:02:47 2011", 
	      "id": 24, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Constellations", 
	      "username": "fred", 
	      "playback_priority": 2, 
	      "user_id": 1, 
	      "artist": "Darwin Deez", 
	      "spotify_url": "spotify:track:3DbEgIX3u7crwCcbOQbcAf", 
	      "length": 187, 
	      "mpd_id": 103, 
	      "user_priority": 25, 
	      "date": "2010", 
	      "title": "The Coma Song", 
	      "time_added": "Sun Dec 11 20:03:39 2011", 
	      "id": 25, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Darwin Deez", 
	      "username": "fred", 
	      "playback_priority": 3, 
	      "user_id": 1, 
	      "artist": "Darwin Deez", 
	      "spotify_url": "spotify:track:2GpgyczUEfniHZdKwvU843", 
	      "length": 186.131, 
	      "mpd_id": 104, 
	      "user_priority": 26, 
	      "date": "2011", 
	      "title": "Bad Day", 
	      "time_added": "Sun Dec 11 20:03:53 2011", 
	      "id": 26, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Feel Good Lost", 
	      "username": "fred", 
	      "playback_priority": 4, 
	      "user_id": 1, 
	      "artist": "Broken Social Scene", 
	      "spotify_url": "spotify:track:6GIV7S7zOxJSxBrNsWaFRZ", 
	      "length": 344.653, 
	      "mpd_id": 105, 
	      "user_priority": 27, 
	      "date": "2004", 
	      "title": "Love And Mathematics", 
	      "time_added": "Sun Dec 11 20:05:19 2011", 
	      "id": 27, 
	      "user": "Fred"
	    }, 

	  ], 
	  "single": "0", 
	  "repeat": "0", 
	  "file": "spotify:track:0b16PJlDwSaBPqM9uyyujg", 
	  "date": "2011-01-01", 
	  "id": "101", 
	  "last_global_playlist_update": 1323654610.545476, 
	  "album": "Codes and Keys", 
	  "artist": "Death Cab for Cutie", 
	  "title": "Monday Morning", 
	  "state": "play", 
	  "response_time": 1323654653.76103, 
	  "time": "259"
	}