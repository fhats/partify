import logging
import time
from functools import wraps

from flask import jsonify, redirect, session, url_for

from mpd_client import mpd_client
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
        with mpd_client() as mpd:
            return f(mpd, *args, **kwargs)
    return wrapped