*******
History
*******

.. contents::

Getting the Track Play History
------------------------------

The play history can be retrieved via :func:`/history <partify.history.history>`. Pagination is supported through the arguments ``ipp``, which specifies the number of items per
page of results, and ``page``, which specifies which page of results to get.

.. autofunction:: partify.history.history
   :noindex:

**Example**

::
	
	GET /history?ipp=10&page=1 HTTP/1.1

::

	{
	  "status":"ok",
	  "tracks":[
	    {
	      "album":"Bee Hives",
	      "length":318.52,
	      "time_played":"2011-12-12T01:00:26.646041",
	      "user":"Fred",
	      "title":"Ambulance For The Ambience",
	      "date":"2004",
	      "artist":"Broken Social Scene",
	      "id":711
	    },
	    {
	      "album":"Bee Hives",
	      "length":429.733,
	      "time_played":"2011-12-12T00:53:16.147733",
	      "user":"Fred",
	      "title":"Da Da Da Da",
	      "date":"2004",
	      "artist":"Broken Social Scene",
	      "id":710
	    },
	    {
	      "album":"Bee Hives",
	      "length":233.707,
	      "time_played":"2011-12-12T00:41:07.001820",
	      "user":"Fred",
	      "title":"hHallmark",
	      "date":"2004",
	      "artist":"Broken Social Scene",
	      "id":709
	    },
	    {
	      "album":"Bee Hives",
	      "length":422.747,
	      "time_played":"2011-12-12T00:34:04.241076",
	      "user":"Fred",
	      "title":"Weddings",
	      "date":"2004",
	      "artist":"Broken Social Scene",
	      "id":708
	    },
	    {
	      "album":"Bee Hives",
	      "length":237.307,
	      "time_played":"2011-12-12T00:30:06.692572",
	      "user":"Fred",
	      "title":"Market Fresh",
	      "date":"2004",
	      "artist":"Broken Social Scene",
	      "id":707
	    },
	    {
	      "album":"Bee Hives",
	      "length":37.12,
	      "time_played":"2011-12-12T00:29:28.743612",
	      "user":"Fred",
	      "title":"Untitled",
	      "date":"2004",
	      "artist":"Broken Social Scene",
	      "id":706
	    },
	    {
	      "album":"Bee Hives",
	      "length":307.053,
	      "time_played":"2011-12-12T00:24:47.266041",
	      "user":"Fred",
	      "title":"Time = Cause",
	      "date":"2004",
	      "artist":"Broken Social Scene",
	      "id":705
	    },
	    {
	      "album":"Passive Me, Aggressive You",
	      "length":109.107,
	      "time_played":"2011-12-12T00:21:41.342349",
	      "user":"Lizzy ",
	      "title":"The Ends",
	      "date":"2011",
	      "artist":"The Naked And Famous",
	      "id":704
	    },
	    {
	      "album":"Find Me a Drink Home",
	      "length":190.64,
	      "time_played":"2011-12-12T00:18:30.502348",
	      "user":"Fred",
	      "title":"Stop Now",
	      "date":"2009",
	      "artist":"Cheap Girls",
	      "id":703
	    },
	    {
	      "album":"Passive Me, Aggressive You",
	      "length":194.36,
	      "time_played":"2011-12-12T00:15:15.912172",
	      "user":"Lizzy ",
	      "title":"A Wolf In Geek's Clothing",
	      "date":"2011",
	      "artist":"The Naked And Famous",
	      "id":702
	    }
	  ],
	  "num_items":10,
	  "pages":72,
	  "response_time":"2011-12-12T05:21:38.966400",
	  "page":1
	}