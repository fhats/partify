*************
Configuration
*************

The following document is intended to provide a guide to configuring Partify to use in a home environment.

**Getting There**

To edit Partify's configuration, you must be logged in to a Partify user account that has administrator configuration modification privileges. If you have just installed Partify, you will get these rights when you register (provided you are the first user to register; subsequent users do not get administrative permissions by default). Once you are logged in, click the "admin" link at the top of any page. You will be taken to a page with, among other things, a section that is title "Configuration". It is in this section that you will want to make the relevant changes.


Stuff You'll Need to Change
---------------------------

* **MPD Server Hostname** - If you aren't sure what to set this to and just installed Partify :ref:`user_manual_installation_easy_way`, simply enter ``localhost``
* **MPD Server Port** - If you aren't sure what to set this to and just installed Partify :ref:`user_manual_installation_easy_way`, simply enter ``6600``
* **Underlying Server Software** - Set this to ``Tornado``

Stuff You Might Want to Change
------------------------------

* **Port to Listen to On** - Set this to ``80`` if you want to be able to access your Partify installation by simply going to http://server instead of http://server:5000
* **Last.fm API Key** - Needed for retrieving images of the currently playing artist. Can be obtained from http://www.last.fm/api/account . If you don't have an API key from Last.fm, go ahead and apply for one. The application process is easy and will immediately approve you for a non-commercial account, which is all you need.

Stuff You Shouldn't Change
--------------------------

* **Hostname to Listen On**

Reference
---------

**MPD Server Hostname** - Tells Partify what hostname to find the Mopidy server on. Required for playing music (Partify does not play music, but relies on Mopidy to do so). Can be any valid hostname string.

*Default:* ``localhost``

**MPD Server Port** - Tells Partify what port the Mopidy server is listening on. Can be an integer from 1-65535. Note that ports 1-1024 are "well known" ports and require administrator privileges to bind to.

*Default:* ``6600``

**Underlying Server Software** - Specifies what web server technology should be used to serve Partify. Can be either ``builtin debugging server`` or ``Tornado``. ``Tornado`` should be used for best results as it is a mature web server technology. ``builtin debugging server`` can be useful for finding problems if you are developing for Partify.

*Default:* ``tornado``

**Hostname to Listen On** - Specifies the hostname that Partify should listen on for incoming connections. ``0.0.0.0`` will listen for connections from other hosts, ``127.0.0.1`` will only listen for connections from the computer that is running Partify.

*Default:* ``0.0.0.0``

**Port to Listen On** - Specifies the port that Partify should listen on for incoming connections.

*Default:* ``5000``

**Last.fm API Key** - Specifies a Last.fm API key that can be used by the player to fetch content from Last.fm, like the now playing artist image. Can be obtained from http://www.last.fm/api/account .

*Default:* ``<blank>``

**Last.fm API Secret** - Specifies a Last.fm API secret. The secret is not currently needed for anything, but may be useful in the future for writing information back to Last.fm, like scrobbling tracks or getting radio data. Can be obtained from http://www.last.fm/api/account .

*Default:* ``<blank>``
