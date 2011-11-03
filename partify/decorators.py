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

from flask import jsonify, redirect, session, url_for

from mpd import MPDClient
from partify import app

def with_authentication(f):
    """A decorator that ensures that a user is logged in and redirects them to a login page if the user is not authenticated.

    The way authentication is currently verified is simply by checking for the user key in session. This is certainly not the best means of 
    authentication but it will do for now. Security is not a high priority for this project since its intended use case is in a local scenario.
    However, it would be great to have better security if time permits."""
    @wraps(f)
    def wrapped():
        if 'user' in session:
            return f()
        else:
            return redirect(url_for('login_form'))
    return wrapped

def with_mpd(f):
    """A decorator that establishes and MPD connection Mopidy and passes it into the wrapped function."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        # TODO: This needs logic to sub in a mock MPD client instead of a real one when the testing flag is up.
        if not app.config['TESTING']:
            mpd_client = MPDClient()
        else:
            from testing.mocks.mock_mpd_client import MockMPDClient
            mpd_client = MockMPDClient()
        mpd_client.connect(**app.config['MPD_SERVER'])
        return_value = f(mpd_client, *args, **kwargs)
        mpd_client.disconnect()
        return return_value
    return wrapped