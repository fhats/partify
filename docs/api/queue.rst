****************
Queue Management
****************

.. contents::

Getting the Global Queue
------------------------

Typically the global play queue is retrieved through the use of :func:`/player/status/poll <partify.player.status>` by setting the parameter ``current`` to none. For more
information, see :ref:`api_get_player_status`.

Getting the User's Queue
------------------------

The user's queue can be retrieved by utilizing either the :func:`/player/status/poll <partify.player.status>` or :func:`/queue/list <partify.queue.list_user_queue>` endpoints.

.. autofunction:: partify.queue.list_user_queue

**Examples**

::

	GET /queue/list HTTP/1.1

::

	{
	  "status": "ok", 
	  "result": [
	    {
	      "album": "Left and Leaving", 
	      "username": "fred", 
	      "playback_priority": 0, 
	      "user_id": 1, 
	      "artist": "The Weakerthans", 
	      "spotify_url": "spotify:track:5xd2GE7yF5Xpb0htiVQonA", 
	      "length": 275.2, 
	      "mpd_id": 109, 
	      "user_priority": 31, 
	      "date": "2000", 
	      "title": "Everything Must Go", 
	      "time_added": "Sun Dec 11 21:18:23 2011", 
	      "id": 31, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Left and Leaving", 
	      "username": "fred", 
	      "playback_priority": 1, 
	      "user_id": 1, 
	      "artist": "The Weakerthans", 
	      "spotify_url": "spotify:track:4FiSkeCUcaraLzEvHUJuVt", 
	      "length": 307.533, 
	      "mpd_id": 110, 
	      "user_priority": 32, 
	      "date": "2000", 
	      "title": "This Is A Fire Door Never Leave Open", 
	      "time_added": "Sun Dec 11 21:18:24 2011", 
	      "id": 32, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Left and Leaving", 
	      "username": "fred", 
	      "playback_priority": 2, 
	      "user_id": 1, 
	      "artist": "The Weakerthans", 
	      "spotify_url": "spotify:track:2BoAdpADIZLtKoCdqcZTBd", 
	      "length": 380.8, 
	      "mpd_id": 111, 
	      "user_priority": 33, 
	      "date": "2000", 
	      "title": "Elegy For Elsabet", 
	      "time_added": "Sun Dec 11 21:18:33 2011", 
	      "id": 33, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Left and Leaving", 
	      "username": "fred", 
	      "playback_priority": 3, 
	      "user_id": 1, 
	      "artist": "The Weakerthans", 
	      "spotify_url": "spotify:track:7bCm0qiuE0RWKV9rHgawfq", 
	      "length": 311, 
	      "mpd_id": 112, 
	      "user_priority": 34, 
	      "date": "2000", 
	      "title": "Exiles Among You", 
	      "time_added": "Sun Dec 11 21:18:35 2011", 
	      "id": 34, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Reconstruction Site", 
	      "username": "fred", 
	      "playback_priority": 4, 
	      "user_id": 1, 
	      "artist": "The Weakerthans", 
	      "spotify_url": "spotify:track:0Ws6AAKyb4YCSVu96GwMda", 
	      "length": 228.866, 
	      "mpd_id": 113, 
	      "user_priority": 35, 
	      "date": "2003", 
	      "title": "Plea From A Cat Named Virtute", 
	      "time_added": "Sun Dec 11 21:18:51 2011", 
	      "id": 35, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Reconstruction Site", 
	      "username": "fred", 
	      "playback_priority": 5, 
	      "user_id": 1, 
	      "artist": "The Weakerthans", 
	      "spotify_url": "spotify:track:4bvDhCqLBZNn4yNdwQhm7s", 
	      "length": 208.933, 
	      "mpd_id": 114, 
	      "user_priority": 36, 
	      "date": "2003", 
	      "title": "Benediction", 
	      "time_added": "Sun Dec 11 21:18:51 2011", 
	      "id": 36, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Reconstruction Site", 
	      "username": "fred", 
	      "playback_priority": 6, 
	      "user_id": 1, 
	      "artist": "The Weakerthans", 
	      "spotify_url": "spotify:track:6SSZckhPUqWCALThQU82Qs", 
	      "length": 172.906, 
	      "mpd_id": 115, 
	      "user_priority": 37, 
	      "date": "2003", 
	      "title": "Time's Arrow", 
	      "time_added": "Sun Dec 11 21:18:54 2011", 
	      "id": 37, 
	      "user": "Fred"
	    }, 
	    {
	      "album": "Reconstruction Site", 
	      "username": "fred", 
	      "playback_priority": 7, 
	      "user_id": 1, 
	      "artist": "The Weakerthans", 
	      "spotify_url": "spotify:track:4OR2Uyz0QCRPYUgLQfSFpO", 
	      "length": 143.693, 
	      "mpd_id": 116, 
	      "user_priority": 38, 
	      "date": "2003", 
	      "title": "Our Retired Explorer", 
	      "time_added": "Sun Dec 11 21:19:13 2011", 
	      "id": 38, 
	      "user": "Fred"
	    }
	  ]
	}


Adding Tracks to the Queue
--------------------------

Tracks are added to the user's play queue using the :func:`/queue/add <partify.queue.add_to_queue>` or :func:`/queue/add_album <partify.queue.add_album_from_track>` endpoints.

.. autofunction:: partify.queue.add_to_queue

.. autofunction:: partify.queue.add_album_from_track

**Examples**

Adding a single track::

	POST /queue/add HTTP/1.1

	spotify_uri:spotify%3Atrack%3A2puGRTU4wKLn6sPF5eUzmR

::

	{
	  "status":"ok",
	  "queue":[
	    {
	      "album":"Left and Leaving",
	      "username":"fred",
	      "playback_priority":0,
	      "user_id":1,
	      "artist":"The Weakerthans",
	      "spotify_url":"spotify:track:7bCm0qiuE0RWKV9rHgawfq",
	      "length":311,
	      "mpd_id":112,
	      "user_priority":34,
	      "date":"2000",
	      "title":"Exiles Among You",
	      "time_added":"Sun Dec 11 21:18:35 2011",
	      "id":34,
	      "user":"Fred"
	    },
	    {
	      "album":"Reconstruction Site",
	      "username":"fred",
	      "playback_priority":2,
	      "user_id":1,
	      "artist":"The Weakerthans",
	      "spotify_url":"spotify:track:0Ws6AAKyb4YCSVu96GwMda",
	      "length":228.866,
	      "mpd_id":113,
	      "user_priority":35,
	      "date":"2003",
	      "title":"Plea From A Cat Named Virtute",
	      "time_added":"Sun Dec 11 21:18:51 2011",
	      "id":35,
	      "user":"Fred"
	    },
	    {
	      "album":"Reconstruction Site",
	      "username":"fred",
	      "playback_priority":4,
	      "user_id":1,
	      "artist":"The Weakerthans",
	      "spotify_url":"spotify:track:4bvDhCqLBZNn4yNdwQhm7s",
	      "length":208.933,
	      "mpd_id":114,
	      "user_priority":36,
	      "date":"2003",
	      "title":"Benediction",
	      "time_added":"Sun Dec 11 21:18:51 2011",
	      "id":36,
	      "user":"Fred"
	    },
	    {
	      "album":"Reconstruction Site",
	      "username":"fred",
	      "playback_priority":6,
	      "user_id":1,
	      "artist":"The Weakerthans",
	      "spotify_url":"spotify:track:6SSZckhPUqWCALThQU82Qs",
	      "length":172.906,
	      "mpd_id":115,
	      "user_priority":37,
	      "date":"2003",
	      "title":"Time's Arrow",
	      "time_added":"Sun Dec 11 21:18:54 2011",
	      "id":37,
	      "user":"Fred"
	    },
	    {
	      "album":"Reconstruction Site",
	      "username":"fred",
	      "playback_priority":8,
	      "user_id":1,
	      "artist":"The Weakerthans",
	      "spotify_url":"spotify:track:4OR2Uyz0QCRPYUgLQfSFpO",
	      "length":143.693,
	      "mpd_id":116,
	      "user_priority":38,
	      "date":"2003",
	      "title":"Our Retired Explorer",
	      "time_added":"Sun Dec 11 21:19:13 2011",
	      "id":38,
	      "user":"Fred"
	    },
	    {
	      "album":"Welcome To The Night Sky",
	      "username":"fred",
	      "playback_priority":10,
	      "user_id":1,
	      "artist":"Wintersleep",
	      "spotify_url":"spotify:track:0XnZkk9X2WxuIbkaKitmAG",
	      "length":216.686,
	      "mpd_id":122,
	      "user_priority":44,
	      "date":"2007",
	      "title":"Archaeologists",
	      "time_added":"Sun Dec 11 21:35:14 2011",
	      "id":44,
	      "user":"Fred"
	    },
	    {
	      "album":"Maladroit",
	      "username":"fred",
	      "playback_priority":15,
	      "user_id":1,
	      "artist":"Weezer",
	      "spotify_url":"spotify:track:2puGRTU4wKLn6sPF5eUzmR",
	      "length":173.333,
	      "mpd_id":128,
	      "user_priority":50,
	      "date":"2002",
	      "title":"Slave",
	      "time_added":"Sun Dec 11 21:45:02 2011",
	      "id":50,
	      "user":"Fred"
	    }
	  ],
	  "file":"spotify:track:2puGRTU4wKLn6sPF5eUzmR"
	}

Adding an album::

	POST /queue/add_album HTTP/1.1

	spotify_files:spotify:track:3qqAHd2rkKWqsWTmVyHF6f
	spotify_files:spotify:track:4BOVyycbgTOSL48RdyfC4W
	spotify_files:spotify:track:1gvS7wlBv8eukeKIQ5CLv2
	spotify_files:spotify:track:7Lh5dqG4jzEHQp6gF2tGsu
	spotify_files:spotify:track:5roFPE3Py2pGvazhNmP24c
	spotify_files:spotify:track:3PdVyPYoC8jj7HwlDrKSHY
	spotify_files:spotify:track:4WCSqIWpeWQps4uma2MKhI
	spotify_files:spotify:track:4MeOUFl4BXoFuoEYrQsuXh
	spotify_files:spotify:track:6PHvKNOVDfNFm52b2G01zk
	spotify_files:spotify:track:39O0msKxtwkPSb3bCvbrBq

::

	{
	  "status":"ok",
	  "queue":[
	    {
	      "album":"Reconstruction Site",
	      "username":"fred",
	      "playback_priority":0,
	      "user_id":1,
	      "artist":"The Weakerthans",
	      "spotify_url":"spotify:track:4bvDhCqLBZNn4yNdwQhm7s",
	      "length":208.933,
	      "mpd_id":114,
	      "user_priority":36,
	      "date":"2003",
	      "title":"Benediction",
	      "time_added":"Sun Dec 11 21:18:51 2011",
	      "id":36,
	      "user":"Fred"
	    },
	    {
	      "album":"Reconstruction Site",
	      "username":"fred",
	      "playback_priority":2,
	      "user_id":1,
	      "artist":"The Weakerthans",
	      "spotify_url":"spotify:track:6SSZckhPUqWCALThQU82Qs",
	      "length":172.906,
	      "mpd_id":115,
	      "user_priority":37,
	      "date":"2003",
	      "title":"Time's Arrow",
	      "time_added":"Sun Dec 11 21:18:54 2011",
	      "id":37,
	      "user":"Fred"
	    },
	    {
	      "album":"Reconstruction Site",
	      "username":"fred",
	      "playback_priority":4,
	      "user_id":1,
	      "artist":"The Weakerthans",
	      "spotify_url":"spotify:track:4OR2Uyz0QCRPYUgLQfSFpO",
	      "length":143.693,
	      "mpd_id":116,
	      "user_priority":38,
	      "date":"2003",
	      "title":"Our Retired Explorer",
	      "time_added":"Sun Dec 11 21:19:13 2011",
	      "id":38,
	      "user":"Fred"
	    },
	    {
	      "album":"Welcome To The Night Sky",
	      "username":"fred",
	      "playback_priority":6,
	      "user_id":1,
	      "artist":"Wintersleep",
	      "spotify_url":"spotify:track:0XnZkk9X2WxuIbkaKitmAG",
	      "length":216.686,
	      "mpd_id":122,
	      "user_priority":44,
	      "date":"2007",
	      "title":"Archaeologists",
	      "time_added":"Sun Dec 11 21:35:14 2011",
	      "id":44,
	      "user":"Fred"
	    },
	    {
	      "album":"Maladroit",
	      "username":"fred",
	      "playback_priority":8,
	      "user_id":1,
	      "artist":"Weezer",
	      "spotify_url":"spotify:track:2puGRTU4wKLn6sPF5eUzmR",
	      "length":173.333,
	      "mpd_id":128,
	      "user_priority":50,
	      "date":"2002",
	      "title":"Slave",
	      "time_added":"Sun Dec 11 21:45:02 2011",
	      "id":50,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":12,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:3qqAHd2rkKWqsWTmVyHF6f",
	      "length":307,
	      "mpd_id":129,
	      "user_priority":51,
	      "date":"2008",
	      "title":"Yuppy Flu",
	      "time_added":"Sun Dec 11 21:58:59 2011",
	      "id":51,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":13,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4BOVyycbgTOSL48RdyfC4W",
	      "length":249,
	      "mpd_id":130,
	      "user_priority":52,
	      "date":"2008",
	      "title":"Death By Fire",
	      "time_added":"Sun Dec 11 21:58:59 2011",
	      "id":52,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":14,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:1gvS7wlBv8eukeKIQ5CLv2",
	      "length":130,
	      "mpd_id":131,
	      "user_priority":53,
	      "date":"2008",
	      "title":"The Man Who Breaks Things (Dark Shuffle)",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":53,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":15,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:7Lh5dqG4jzEHQp6gF2tGsu",
	      "length":221,
	      "mpd_id":132,
	      "user_priority":54,
	      "date":"2008",
	      "title":"Some Are Lakes",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":54,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":16,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:5roFPE3Py2pGvazhNmP24c",
	      "length":266,
	      "mpd_id":133,
	      "user_priority":55,
	      "date":"2008",
	      "title":"Give Me Back My Heart Attack",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":55,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":17,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:3PdVyPYoC8jj7HwlDrKSHY",
	      "length":294,
	      "mpd_id":134,
	      "user_priority":56,
	      "date":"2008",
	      "title":"It's Okay",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":56,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":18,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4WCSqIWpeWQps4uma2MKhI",
	      "length":225,
	      "mpd_id":135,
	      "user_priority":57,
	      "date":"2008",
	      "title":"Young Bridge",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":57,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":19,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4MeOUFl4BXoFuoEYrQsuXh",
	      "length":194,
	      "mpd_id":136,
	      "user_priority":58,
	      "date":"2008",
	      "title":"Corner Phone",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":58,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":20,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:6PHvKNOVDfNFm52b2G01zk",
	      "length":259,
	      "mpd_id":137,
	      "user_priority":59,
	      "date":"2008",
	      "title":"Got A Call",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":59,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":21,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:39O0msKxtwkPSb3bCvbrBq",
	      "length":202,
	      "mpd_id":138,
	      "user_priority":60,
	      "date":"2008",
	      "title":"Troubled",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":60,
	      "user":"Fred"
	    }
	  ]
	}


Reordering the User's Queue
---------------------------

The user's queue can be re-ordered by issuing a ``POST`` to :func:`/queue/reorder <partify.queue.reorder_queue>` with a list of track:position mappings in the request body.
The new positions will be updated in the database and will be updated in the Mopidy play queue on the next round of consistency checking.

.. note:: Right now it is preferable to provide every track in the user's play queue and the new position for that track to avoid problems regarding tracks with the same
   priority in the user's queue (this is what the built-in client currently does).

.. autofunction:: partify.queue.reorder_queue

**Examples**

::

	POST /queue/reorder HTTP/1.1

	44:1
	50:12
	51:2
	52:3
	53:4
	54:5
	55:6
	56:7
	57:8
	58:9
	59:10
	60:11

::

	{
	  "status":"ok",
	  "queue":[
	    {
	      "album":"Welcome To The Night Sky",
	      "username":"fred",
	      "playback_priority":0,
	      "user_id":1,
	      "artist":"Wintersleep",
	      "spotify_url":"spotify:track:0XnZkk9X2WxuIbkaKitmAG",
	      "length":216.686,
	      "mpd_id":122,
	      "user_priority":1,
	      "date":"2007",
	      "title":"Archaeologists",
	      "time_added":"Sun Dec 11 21:35:14 2011",
	      "id":44,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":4,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:3qqAHd2rkKWqsWTmVyHF6f",
	      "length":307,
	      "mpd_id":129,
	      "user_priority":2,
	      "date":"2008",
	      "title":"Yuppy Flu",
	      "time_added":"Sun Dec 11 21:58:59 2011",
	      "id":51,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":6,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4BOVyycbgTOSL48RdyfC4W",
	      "length":249,
	      "mpd_id":130,
	      "user_priority":3,
	      "date":"2008",
	      "title":"Death By Fire",
	      "time_added":"Sun Dec 11 21:58:59 2011",
	      "id":52,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":8,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:1gvS7wlBv8eukeKIQ5CLv2",
	      "length":130,
	      "mpd_id":131,
	      "user_priority":4,
	      "date":"2008",
	      "title":"The Man Who Breaks Things (Dark Shuffle)",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":53,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":9,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:7Lh5dqG4jzEHQp6gF2tGsu",
	      "length":221,
	      "mpd_id":132,
	      "user_priority":5,
	      "date":"2008",
	      "title":"Some Are Lakes",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":54,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":10,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:5roFPE3Py2pGvazhNmP24c",
	      "length":266,
	      "mpd_id":133,
	      "user_priority":6,
	      "date":"2008",
	      "title":"Give Me Back My Heart Attack",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":55,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":11,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:3PdVyPYoC8jj7HwlDrKSHY",
	      "length":294,
	      "mpd_id":134,
	      "user_priority":7,
	      "date":"2008",
	      "title":"It's Okay",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":56,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":12,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4WCSqIWpeWQps4uma2MKhI",
	      "length":225,
	      "mpd_id":135,
	      "user_priority":8,
	      "date":"2008",
	      "title":"Young Bridge",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":57,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":13,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4MeOUFl4BXoFuoEYrQsuXh",
	      "length":194,
	      "mpd_id":136,
	      "user_priority":9,
	      "date":"2008",
	      "title":"Corner Phone",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":58,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":14,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:6PHvKNOVDfNFm52b2G01zk",
	      "length":259,
	      "mpd_id":137,
	      "user_priority":10,
	      "date":"2008",
	      "title":"Got A Call",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":59,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":15,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:39O0msKxtwkPSb3bCvbrBq",
	      "length":202,
	      "mpd_id":138,
	      "user_priority":11,
	      "date":"2008",
	      "title":"Troubled",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":60,
	      "user":"Fred"
	    },
	    {
	      "album":"Maladroit",
	      "username":"fred",
	      "playback_priority":2,
	      "user_id":1,
	      "artist":"Weezer",
	      "spotify_url":"spotify:track:2puGRTU4wKLn6sPF5eUzmR",
	      "length":173.333,
	      "mpd_id":128,
	      "user_priority":12,
	      "date":"2002",
	      "title":"Slave",
	      "time_added":"Sun Dec 11 21:45:02 2011",
	      "id":50,
	      "user":"Fred"
	    }
	  ]
	}

Removing Tracks from the Queue
------------------------------

Tracks can be removed from the user's play queue by sending the queue entry's ID in a ``POST`` request to :func:`/queue/remove <partify.queue.remove_from_queue>`.

.. autofunction:: partify.queue.remove_from_queue

**Examples**

::

	POST /queue/remove HTTP/1.1
	
	track_id:140
	
::

	{
	  "status":"ok",
	  "queue":[
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":0,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:3qqAHd2rkKWqsWTmVyHF6f",
	      "length":307,
	      "mpd_id":129,
	      "user_priority":2,
	      "date":"2008",
	      "title":"Yuppy Flu",
	      "time_added":"Sun Dec 11 21:58:59 2011",
	      "id":51,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":2,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4BOVyycbgTOSL48RdyfC4W",
	      "length":249,
	      "mpd_id":130,
	      "user_priority":3,
	      "date":"2008",
	      "title":"Death By Fire",
	      "time_added":"Sun Dec 11 21:58:59 2011",
	      "id":52,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":4,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:1gvS7wlBv8eukeKIQ5CLv2",
	      "length":130,
	      "mpd_id":131,
	      "user_priority":4,
	      "date":"2008",
	      "title":"The Man Who Breaks Things (Dark Shuffle)",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":53,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":6,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:7Lh5dqG4jzEHQp6gF2tGsu",
	      "length":221,
	      "mpd_id":132,
	      "user_priority":5,
	      "date":"2008",
	      "title":"Some Are Lakes",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":54,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":7,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:5roFPE3Py2pGvazhNmP24c",
	      "length":266,
	      "mpd_id":133,
	      "user_priority":6,
	      "date":"2008",
	      "title":"Give Me Back My Heart Attack",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":55,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":8,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:3PdVyPYoC8jj7HwlDrKSHY",
	      "length":294,
	      "mpd_id":134,
	      "user_priority":7,
	      "date":"2008",
	      "title":"It's Okay",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":56,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":9,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4WCSqIWpeWQps4uma2MKhI",
	      "length":225,
	      "mpd_id":135,
	      "user_priority":8,
	      "date":"2008",
	      "title":"Young Bridge",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":57,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":10,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:4MeOUFl4BXoFuoEYrQsuXh",
	      "length":194,
	      "mpd_id":136,
	      "user_priority":9,
	      "date":"2008",
	      "title":"Corner Phone",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":58,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":11,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:6PHvKNOVDfNFm52b2G01zk",
	      "length":259,
	      "mpd_id":137,
	      "user_priority":10,
	      "date":"2008",
	      "title":"Got A Call",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":59,
	      "user":"Fred"
	    },
	    {
	      "album":"Some Are Lakes",
	      "username":"fred",
	      "playback_priority":12,
	      "user_id":1,
	      "artist":"Land Of Talk",
	      "spotify_url":"spotify:track:39O0msKxtwkPSb3bCvbrBq",
	      "length":202,
	      "mpd_id":138,
	      "user_priority":11,
	      "date":"2008",
	      "title":"Troubled",
	      "time_added":"Sun Dec 11 21:59:00 2011",
	      "id":60,
	      "user":"Fred"
	    },
	    {
	      "album":"Maladroit",
	      "username":"fred",
	      "playback_priority":13,
	      "user_id":1,
	      "artist":"Weezer",
	      "spotify_url":"spotify:track:2puGRTU4wKLn6sPF5eUzmR",
	      "length":173.333,
	      "mpd_id":128,
	      "user_priority":12,
	      "date":"2002",
	      "title":"Slave",
	      "time_added":"Sun Dec 11 21:45:02 2011",
	      "id":50,
	      "user":"Fred"
	    },
	    {
	      "album":"Live It Out",
	      "username":"fred",
	      "playback_priority":14,
	      "user_id":1,
	      "artist":"Metric",
	      "spotify_url":"spotify:track:274wSNXxlqeMypM5gKkohe",
	      "length":262.147,
	      "mpd_id":140,
	      "user_priority":50,
	      "date":"2005",
	      "title":"Too Little Too Late",
	      "time_added":"Sun Dec 11 22:33:35 2011",
	      "id":61,
	      "user":"Fred"
	    }
	  ]
	} 
