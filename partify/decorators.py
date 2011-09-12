import logging
import time
from functools import wraps

from flask import jsonify

from mpd_client import mpd_client
from partify import app

def default_json(f):
    @wraps(f)
    def wrapped():
        return jsonify(status=f())
    return wrapped

def with_mpd(f):
    @wraps(f)
    def wrapped():
        with mpd_client() as mpd:
            return f(mpd)
    return wrapped