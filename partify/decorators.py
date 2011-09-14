import logging
import time
from functools import wraps

from flask import jsonify, session

from mpd_client import mpd_client
from partify import app

def default_json(f):
    @wraps(f)
    def wrapped():
        return jsonify(status=f())
    return wrapped

# This is really poor authentication. Good thing it doesn't really matter!
def with_authentication(f):
	@wraps(f)
	def wrapped():
		if 'user' in session:
			return f()
		else:
			return redirect_url('login_form')
	return wrapped

def with_mpd(f):
    @wraps(f)
    def wrapped():
        with mpd_client() as mpd:
            return f(mpd)
    return wrapped