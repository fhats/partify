*********
Searching
*********

.. contents::

Searching the Library
---------------------

To search through the Mopidy catalog for available tracks, send a ``GET`` request to :func:`/track/search <partify.track.track_search>` with at least one of
the following parameters:

* **artist** - Specifies the artist to search for
* **title** - Specifies the title of the track to search for
* **album** - Specifies the album to search for

A list of results will be provided, from which you can find Spotify URLs to use with :func:`/queue/add <partify.queue.add_to_queue>` . Results will be returned as 
sorted by a crude relevance function, then by artist, then by album. 

.. autofunction:: partify.track.track_search
   :noindex:

**Examples**

::

	GET /track/search?artist=Lemuria&album=Get+Better HTTP/1.1

::

	{
	  "status":"ok",
	  "results":[
	    {
	      "album":"Get Better",
	      "title":"Pants",
	      "track":"1",
	      "artist":"Lemuria",
	      "file":"spotify:track:6kc2oB01BdngotWCDICoFP",
	      "time":"160",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Yesterday's Lunch",
	      "track":"2",
	      "artist":"Lemuria",
	      "file":"spotify:track:6Wvkb8YMiHcz9i81KqS7In",
	      "time":"200",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Lipstick",
	      "track":"3",
	      "artist":"Lemuria",
	      "file":"spotify:track:03n9nvTnY9XML1Deh3Ykt8",
	      "time":"177",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Buzz",
	      "track":"4",
	      "artist":"Lemuria",
	      "file":"spotify:track:7kCjLp4r7CIHS4Lz52lSsC",
	      "time":"182",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Wardrobe",
	      "track":"5",
	      "artist":"Lemuria",
	      "file":"spotify:track:2Jke9IRAzOClf2JupBrWKf",
	      "time":"118",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Length Away",
	      "track":"6",
	      "artist":"Lemuria",
	      "file":"spotify:track:3Y69AIjyQ4KjhIzXdKLfTb",
	      "time":"160",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Dog",
	      "track":"7",
	      "artist":"Lemuria",
	      "file":"spotify:track:5b9N7NgZheNvlhHyQ5nQrD",
	      "time":"122",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Dogs",
	      "track":"8",
	      "artist":"Lemuria",
	      "file":"spotify:track:0rFoZlyDdGAiJPVN2uYhCH",
	      "time":"80",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Get Some Sleep",
	      "track":"9",
	      "artist":"Lemuria",
	      "file":"spotify:track:2UmFn3JnZjTzPA3pzy2FwG",
	      "time":"104",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Hawaiian T-Shirt",
	      "track":"10",
	      "artist":"Lemuria",
	      "file":"spotify:track:6FFDIDls7YxsjbX234QYh4",
	      "time":"151",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Fingers",
	      "track":"11",
	      "artist":"Lemuria",
	      "file":"spotify:track:2yXaGqxnlObRWesoUUmGGG",
	      "time":"103",
	      "date":"2008-01-01"
	    },
	    {
	      "album":"Get Better",
	      "title":"Mechanical",
	      "track":"12",
	      "artist":"Lemuria",
	      "file":"spotify:track:5Zjuc0GUmyDyrXsKu8uxt5",
	      "time":"164",
	      "date":"2008-01-01"
	    }
	  ]
	}