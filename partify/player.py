import json
import random
import select
import time

from flask import Response, jsonify, redirect, render_template, session, url_for

from decorators import with_mpd
from partify import app
from partify.models import PlayQueueEntry
from partify.models import Track

@app.route('/player', methods=['GET'])
def player():
    if 'user' in session:
        # User is logged in
        # TODO: Move all this stuff into the frontend via AJAX (see #8, #9)
        # Pull the user's play queue
        users_tracks = PlayQueueEntry.query.filter(PlayQueueEntry.user_id == session['user']['id'])
        global_queue = PlayQueueEntry.query.order_by(PlayQueueEntry.playback_priority).all()

        return render_template("player.html", user_play_queue=users_tracks, global_play_queue=global_queue)
    else:
        return redirect(url_for('login_form'))

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
        status[key] = current_song.get(key, 0 if key == 'time' else '')
    for key in ('state', 'volume', 'elapsed'):
        status[key] = player_status.get(key, 0 if key == 'elapsed' else '')

    # Throw in a timestamp to assist synchronization
    status['response_time'] = time.time()

    return status