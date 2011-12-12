**********
Statistics
**********

.. contents::

Getting Statistics
------------------

A set of statistics about the player history can be retrieved from :func:`/statistics <partify.statistics.statistics>` . Statistics for the last day, week, month, year, and for
all time will be returned.

.. autofunction:: partify.statistics.statistics
   :noindex:

**Examples**

::

	GET /statistics HTTP/1.1

::

	{
	  "status":"ok",
	  "statistics":{
	    "week":{
	      "total_time":96778.54400000005,
	      "total_tracks":378,
	      "top_albums":{
	        "1":{
	          "album":"Hybrid Theory",
	          "plays":16,
	          "artist":"Linkin Park"
	        },
	        "2":{
	          "album":"Good Apollo, I'm Burning Star IV, Volume One:  From Fear Through The Eyes Of Madness",
	          "plays":15,
	          "artist":"Coheed and Cambria"
	        },
	        "3":{
	          "album":"The Second Stage Turbine Blade",
	          "plays":14,
	          "artist":"Coheed and Cambria"
	        },
	        "4":{
	          "album":"Mind Elevation",
	          "plays":13,
	          "artist":"Nightmares On Wax"
	        }
	      },
	      "top_users":{
	        "1":{
	          "username":"littlelizzy",
	          "plays":165,
	          "user":"Lizzy "
	        },
	        "2":{
	          "username":"fred",
	          "plays":70,
	          "user":"Fred"
	        },
	        "3":{
	          "username":"sjotp",
	          "plays":63,
	          "user":"Steve Johnson"
	        },
	        "4":{
	          "username":"tlg14",
	          "plays":51,
	          "user":"Tyler"
	        }
	      },
	      "top_artists":{
	        "1":{
	          "plays":38,
	          "artist":"Coheed and Cambria"
	        },
	        "2":{
	          "plays":37,
	          "artist":"Nightmares On Wax"
	        },
	        "3":{
	          "plays":34,
	          "artist":"God Is An Astronaut"
	        },
	        "4":{
	          "plays":16,
	          "artist":"Linkin Park"
	        }
	      }
	    },
	    "all":{
	      "total_time":170454.3739999996,
	      "total_tracks":711,
	      "top_albums":{
	        "1":{
	          "album":"xx",
	          "plays":22,
	          "artist":"The xx"
	        },
	        "2":{
	          "album":"Welcome To The Night Sky",
	          "plays":20,
	          "artist":"Wintersleep"
	        },
	        "3":{
	          "album":"Good Apollo, I'm Burning Star IV, Volume One:  From Fear Through The Eyes Of Madness",
	          "plays":18,
	          "artist":"Coheed and Cambria"
	        },
	        "4":{
	          "album":"The First Collection 2005-2006",
	          "plays":18,
	          "artist":"Lemuria"
	        }
	      },
	      "top_users":{
	        "1":{
	          "username":"fred",
	          "plays":289,
	          "user":"Fred"
	        },
	        "2":{
	          "username":"littlelizzy",
	          "plays":177,
	          "user":"Lizzy "
	        },
	        "3":{
	          "username":"tlg14",
	          "plays":117,
	          "user":"Tyler"
	        },
	        "4":{
	          "username":"sjotp",
	          "plays":63,
	          "user":"Steve Johnson"
	        }
	      },
	      "top_artists":{
	        "1":{
	          "plays":41,
	          "artist":"Coheed and Cambria"
	        },
	        "2":{
	          "plays":37,
	          "artist":"Nightmares On Wax"
	        },
	        "3":{
	          "plays":34,
	          "artist":"God Is An Astronaut"
	        },
	        "4":{
	          "plays":33,
	          "artist":"Lemuria"
	        }
	      }
	    },
	    "month":{
	      "total_time":170454.3739999996,
	      "total_tracks":711,
	      "top_albums":{
	        "1":{
	          "album":"xx",
	          "plays":22,
	          "artist":"The xx"
	        },
	        "2":{
	          "album":"Welcome To The Night Sky",
	          "plays":20,
	          "artist":"Wintersleep"
	        },
	        "3":{
	          "album":"Good Apollo, I'm Burning Star IV, Volume One:  From Fear Through The Eyes Of Madness",
	          "plays":18,
	          "artist":"Coheed and Cambria"
	        },
	        "4":{
	          "album":"The First Collection 2005-2006",
	          "plays":18,
	          "artist":"Lemuria"
	        }
	      },
	      "top_users":{
	        "1":{
	          "username":"fred",
	          "plays":289,
	          "user":"Fred"
	        },
	        "2":{
	          "username":"littlelizzy",
	          "plays":177,
	          "user":"Lizzy "
	        },
	        "3":{
	          "username":"tlg14",
	          "plays":117,
	          "user":"Tyler"
	        },
	        "4":{
	          "username":"sjotp",
	          "plays":63,
	          "user":"Steve Johnson"
	        }
	      },
	      "top_artists":{
	        "1":{
	          "plays":41,
	          "artist":"Coheed and Cambria"
	        },
	        "2":{
	          "plays":37,
	          "artist":"Nightmares On Wax"
	        },
	        "3":{
	          "plays":34,
	          "artist":"God Is An Astronaut"
	        },
	        "4":{
	          "plays":33,
	          "artist":"Lemuria"
	        }
	      }
	    },
	    "day":{
	      "total_time":22698.194000000003,
	      "total_tracks":89,
	      "top_albums":{
	        "1":{
	          "album":"Mind Elevation",
	          "plays":13,
	          "artist":"Nightmares On Wax"
	        },
	        "2":{
	          "album":"Passive Me, Aggressive You",
	          "plays":12,
	          "artist":"The Naked And Famous"
	        },
	        "3":{
	          "album":"Thought So\u2026",
	          "plays":11,
	          "artist":"Nightmares On Wax"
	        },
	        "4":{
	          "album":"Carboot Soul",
	          "plays":10,
	          "artist":"Nightmares On Wax"
	        }
	      },
	      "top_users":{
	        "1":{
	          "username":"littlelizzy",
	          "plays":40,
	          "user":"Lizzy "
	        },
	        "2":{
	          "username":"sjotp",
	          "plays":23,
	          "user":"Steve Johnson"
	        },
	        "3":{
	          "username":"fred",
	          "plays":21,
	          "user":"Fred"
	        },
	        "4":{
	          "username":"tlg14",
	          "plays":5,
	          "user":"Tyler"
	        }
	      },
	      "top_artists":{
	        "1":{
	          "plays":37,
	          "artist":"Nightmares On Wax"
	        },
	        "2":{
	          "plays":12,
	          "artist":"The Naked And Famous"
	        },
	        "3":{
	          "plays":8,
	          "artist":"Broken Social Scene"
	        },
	        "4":{
	          "plays":5,
	          "artist":"Manchester Orchestra"
	        }
	      }
	    },
	    "year":{
	      "total_time":170454.3739999996,
	      "total_tracks":711,
	      "top_albums":{
	        "1":{
	          "album":"xx",
	          "plays":22,
	          "artist":"The xx"
	        },
	        "2":{
	          "album":"Welcome To The Night Sky",
	          "plays":20,
	          "artist":"Wintersleep"
	        },
	        "3":{
	          "album":"Good Apollo, I'm Burning Star IV, Volume One:  From Fear Through The Eyes Of Madness",
	          "plays":18,
	          "artist":"Coheed and Cambria"
	        },
	        "4":{
	          "album":"The First Collection 2005-2006",
	          "plays":18,
	          "artist":"Lemuria"
	        }
	      },
	      "top_users":{
	        "1":{
	          "username":"fred",
	          "plays":289,
	          "user":"Fred"
	        },
	        "2":{
	          "username":"littlelizzy",
	          "plays":177,
	          "user":"Lizzy "
	        },
	        "3":{
	          "username":"tlg14",
	          "plays":117,
	          "user":"Tyler"
	        },
	        "4":{
	          "username":"sjotp",
	          "plays":63,
	          "user":"Steve Johnson"
	        }
	      },
	      "top_artists":{
	        "1":{
	          "plays":41,
	          "artist":"Coheed and Cambria"
	        },
	        "2":{
	          "plays":37,
	          "artist":"Nightmares On Wax"
	        },
	        "3":{
	          "plays":34,
	          "artist":"God Is An Astronaut"
	        },
	        "4":{
	          "plays":33,
	          "artist":"Lemuria"
	        }
	      }
	    }
	  },
	  "response_time":"2011-12-12T05:21:38.777453"
	}
