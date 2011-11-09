"""Copyright 2011 Fred Hatfull

This file is part of Partify.

Partify is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Partify is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Partify.  If not, see <http://www.gnu.org/licenses/>."""

import logging
import time
from functools import wraps

from flask import flash, jsonify, redirect, session, url_for

from mpd import MPDClient
from ipc import get_mpd_lock, release_mpd_lock
from partify import app
from partify.priv import user_has_privilege

def with_authentication(f):
    """A decorator that ensures that a user is logged in and redirects them to a login page if the user is not authenticated.

    The way authentication is currently verified is simply by checking for the user key in session. This is certainly not the best means of 
    authentication but it will do for now. Security is not a high priority for this project since its intended use case is in a local scenario.
    However, it would be great to have better security if time permits."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_form'))
    return wrapped

def with_mpd(f):
    """A decorator that establishes and MPD connection Mopidy and passes it into the wrapped function."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not app.config['TESTING']:
            mpd_client = MPDClient()
        else:
            from testing.mocks.mock_mpd_client import MockMPDClient
            mpd_client = MockMPDClient()
        try:
            mpd_client.connect(host=app.config['MPD_SERVER_HOSTNAME'], port=app.config['MPD_SERVER_PORT'])
        except:
            # Do something sensible when you can't connect to the MPD server, like pass None in for mpd_client
            # maybe eventually just forward to the configuration page/no connection page
            mpd_client = None
            app.logger.warning("Could not connect to MPD server on host %r, port %r" % (app.config['MPD_SERVER_HOSTNAME'], app.config['MPD_SERVER_PORT']))
            try:
                return jsonify(status="error", message="MPD credentials incorrect")
            except:
                return "Crap.", 500
        else:
            return_value = f(mpd_client, *args, **kwargs)
            if mpd_client is not None:
                mpd_client.disconnect()
            return return_value
    return wrapped

def with_mpd_lock(f):
    """A decorator that ensures that no two functions that send commands to MPD happen simultaneously."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        get_mpd_lock()
        rv = f(*args, **kwargs)
        release_mpd_lock()
        return rv
    return wrapped

def with_privileges(privs, fail_mode="json"):
    """A decorator that restricts access to the decorated endpoint if the logged in user does not have sufficient privileges."""
    def dec(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            current_user = session['user']['id']
            missing_privs = [p for p in privs if not user_has_privilege(current_user, p)]
            if len(missing_privs) == 0:
                return f(*args, **kwargs)
            else:
                if fail_mode == "redirect":
                    return redirect(url_for("player"))
                elif fail_mode == "json":
                    return jsonify(status="error", message="You are not authorized to view this page!"), 403
                else:
                    return jsonify(status="Not authorized."), 403
        return wrapped
    return dec
