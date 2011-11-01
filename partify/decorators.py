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
        try:
            mpd_client.connect(host=app.config['MPD_SERVER_HOSTNAME'], port=app.config['MPD_SERVER_PORT'])
        except:
            # Do something sensible when you can't connect to the MPD server, like pass None in for mpd_client
            # maybe eventually just forward to the configuration page/no connection page
            mpd_client = None
            app.logger.warning("Could not connect to MPD server on host %r, port %r" % (app.config['MPD_SERVER_HOSTNAME'], app.config['MPD_SERVER_PORT']))
        else:
            return_value = f(mpd_client, *args, **kwargs)
            if mpd_client is not None:
                mpd_client.disconnect()
            return return_value
    return wrapped