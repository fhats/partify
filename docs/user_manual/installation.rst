************
Installation
************

This page is intended to help you get started using Partify. If you have any problems or questions, please don't hesitate to email me at `fred.hatfull@gmail.com <mailto:fred.hatfull@gmail.com>`_ or to join ``#partify`` on `irc.freenode.net <http://freenode.net/>`_.

Installation is roughly divided into two paths: :ref:`user_manual_installation_easy_way` and :ref:`user_manual_installation_hard_way`
(developers can get started with the latest source by reading :ref:`user_manual_installation_from_source`).

.. _user_manual_installation_easy_way:

The Easy Way
------------

Installation of Partify and Mopidy on Ubuntu Linux systems is as easy as running an automated shell script. This script is currently targeted toward Ubuntu systems and is only tested against Ubuntu 11.04 (but should work in theory with any recent Ubuntu version). For installation on other operating systems, see :ref:`user_manual_installation_hard_way`.

To install Partify on Ubuntu, simply run the following command in a terminal:

::

	wget http://partify.us/static/scripts/install_ubuntu.sh ; chmod +x ./install_ubuntu.sh ; sudo ./install_ubuntu.sh

The script will download and install `Mopidy <http://www.mopidy.com>`_, the music player that does the heavy lifting of streaming music from Spotify; download and install the tools needed to install Partify; prompt you for your `Spotify Premium <http://www.spotify.com/us/get-spotify/overview/>`_ account details; set up Mopidy and Partify to run when Ubuntu starts up; and starts Mopidy and Partify.

Congratulations! You are almost ready to start jamming! After you have run the installation script you should point your web browser at http://127.0.0.1:5000/ proceed to the :doc:`configuration` page.

For technical individuals, a few notes about this script:

* Much to your anticipated chagrin, the Spotify username and password provided by this script are eventually **stored in plaintext**. This is a limitation of Mopidy, as it needs to read the username and password out of an internal configuration file that this script sets up for you. A fortunate mitigation of this issue is that the authentication credentials are stored in /root, a directory that is by default read-protected from users that are not root and don't have sudo. While this is no substitute for a properly protected password, I cannot work around this limitation right now. In the near future this will probably be fixed by the Mopidy maintainers.

* This script sets up Mopidy and Partify to be running as root. This is not ideal but was the fastest way to get an easy distribution solution working, and is a tradeoff that was made under the assumption that the vast majority of installations would be on local networks. That said, Partify is not hardened in terms of security and by default serves from the built-in server included with Flask. **If your system is public-facing**, make sure to disallow non-local connections on the port Partify is running on (by default 5000) and set up the server to use the Tornado server (see :doc:`configuration`). If you choose to allow connections from non-local hosts to Partify, do so **at your own risk!**

* Along the same lines, Partify installs all of its dependencies as system packages, not in a virtualenv. This is done to simplify installation. This is frowned upon by many Pythonistas, but if you are one of those people then you probably won't obejct to :ref:`user_manual_installation_hard_way` any way.

.. _user_manual_installation_hard_way:

The Hard(er) Way
----------------

Partify itself is not too difficult to install, but Mopidy may present other challenges. This guide assumes you have a working Mopidy server running, and will only cover Partify installation. For details on getting Mopidy set up and running, see the `Mopidy documentation <http://www.mopidy.com/docs/master/>`_.

The first thing you should do is make sure that you are running a version of Python needed to run Partify. You can check this by opening a terminal and typing:

::

    python --version

You should get a response that looks something like ``Python 2.7.1``. If the number reported by this command is less than 2.6, you should upgrade to a later version of Python, which can be downloaded from `the Python website <http://python.org/download/>`_.

Installing Partify and its dependencies is not, in fact, difficult. If you are looking for the most painless install method, simply install Partify using ``easy_install`` as root:

::

    sudo easy_install partify

or on Windows:

::

    easy_install partify

Note that doing so will install Partify and its dependencies as system packages, which may not be ideal if you are running projects which use different versions of Partify's dependencies. To avoid this one can use a virtualenv, which is documented at its `PyPI page <http://pypi.python.org/pypi/virtualenv>`_. If you aren't sure how to do this or aren't sure if you have any installed applications that will conflict with Partify, simply try the command above.

You will now have a new application on your system called ``run_partify``. Executing this command will start Partify. This command can be wrapped in initialization scripts that are pertinent to your operating system in order to start Partify when your computer starts. Example Ubuntu upstart scripts can be found at http://partify.us/static/scripts/partify.conf and http://partify.us/static/scripts/mopidy.conf

Execute ``run_partify``, point your web browser at http://127.0.0.1:5000/ , and head on over to the :doc:`configuration` page.

.. _user_manual_installation_from_source:

From Source
-----------

Partify can also be installed from source if you want to be running the latest, potentially unstable code. This section is intended for people who know what they are doing; if you aren't comfortable with the procedure outlined here, trying installing :ref:`user_manual_installation_easy_way` or :ref:`user_manual_installation_hard_way`. To my knowledge this only works on OSX/Linux at this time, but I'm sure it could be made to work for Windows. Getting Coffeescript to work on Windows can be finnicky and you'll need some version of make, but otherwise everything *should* run fine on Windows...

**What You Need**

* git
* python 2.6 or later
* python setuptools 

**Install the Dependencies**

Either in a virtualenv or as root, install the following Python packages:

* Flask
* Flask-WTF
* Flask-SQLAlchemy
* Tornado

::

    easy_install flask flask-sqlalchemy flask-wtf tornado

Next, install Coffeescript. To do so, you need Node.js:

(from http://nodejs.org/#download)

::

    mkdir ~/sources
    cd ~/sources
    git clone git://github.com/joyent/node.git
    cd node
    git checkout v0.4.11
    export JOBS=2
    mkdir ~/local
    ./configure --prefix=$HOME/local/node
    make
    make install
    echo 'export PATH=$HOME/local/node/bin:$PATH' >> ~/.profile
    echo 'export NODE_PATH=$HOME/local/node:$HOME/local/node/lib/node_modules' >> ~/.profile
    source ~/.profile

Install NPM, the Node.js Package Manager

(from http://npmjs.org/)

::

    curl http://npmjs.org/install.sh | sh

Finally, install Coffeescript

::

    npm install -g coffee-script

**Download the Source**

Make a directory where you can keep the Partify source and change to it. I call mine `sources`:

::

    mkdir ~/sources
    cd ~/sources

Download the source from the Partify git repository:

::

    git clone git://github.com/fxh32/partify.git

**Pick your version**

By default, the master branch of the repository will be checked out. For different versions of the code, check out a different branch:

* `master` - Contains the latest stable code from the last version milestone.
* `develop` - Contains the latest semi-stable code that has been committed towards the next milestone. Typically ahead of `master` and has branches folded into it when they close issues. Generally usable but not guaranteed not to break things.
* `<name>_<issue_number>` - a branch containing work on the issue `<name>` with issue number `<issue_number>`. Very likely to break things if `<issue_number>` has not been closed yet

::

    git checkout (master|develop|<name>_<issue_number>)

Of course, you can at any time make sure you are up to date with the latest code on Github by issuing

::

    git pull

**Run Partify**

The last step that needs to happen before you can run Partify is compilation of the Coffeescript into Javascript assets. This can be done by simply issuing

::

    make

You can now run Partify!

::

    run_partify

*Please note: the preceding instruction to install Partify from source were compiled from memory and should be fairly accurate; however, if you spot any discrepancies or have any trouble, please let me know.*