import json
import random
import select
import time

from flask import jsonify, Response

from decorators import with_mpd
from partify import app

@app.route('/player/status/poll', methods=['GET'])
@with_mpd
def status(mpd):
	return jsonify(_get_status(mpd))

@app.route('/player/status/idle')
@with_mpd
def idle(mpd):
	mpd.send_idle()
	select.select([mpd], [], [])
	changed = mpd.fetch_idle()
	status = _get_status(mpd)
	event = "event: %s\ndata: %s" % (changed[0], json.dumps(status))
	app.logger.debug(event)
	return Response(event, mimetype='text/event-stream', direct_passthrough=True)

def _get_status(mpd):
	"""Get the entire player status needed for the front end."""
	# Get the player status
	player_status = mpd.status()
	# Get the current song
	current_song = mpd.currentsong()

	status = {}
	for key in ('title', 'artist', 'album', 'date', 'file', 'time'):
		status[key] = current_song[key]
	for key in ('state', 'volume', 'elapsed'):
		status[key] = player_status[key]

	# Throw in a timestamp to assist synchronization
	status['response_time'] = time.time()

	return status