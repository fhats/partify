import random
import select
import time

from flask import jsonify, Response

from decorators import with_mpd
from partify import app

@app.route('/player/status', methods=['GET'])
@with_mpd
def status(mpd):
	mpd.send_idle()
	select.select([mpd], [], [])
	changed = mpd.fetch_idle()
	return Response("data: %r" % changed, mimetype='text/event-stream')