import json
import random
import select
import time
from math import ceil

from flask import Response, jsonify, redirect, render_template, request, session, url_for

from decorators import with_authentication, with_mpd
from partify import app, last_updated
from partify.models import PlayQueueEntry
from partify.models import Track

@app.route('/player', methods=['GET'])
@with_authentication
def player():
    """Display the player page.

    Sends the user's queue and the global queue along and displays the player page."""
    users_tracks = get_user_queue(session['user']['id'])
    global_queue = get_global_queue()

    return render_template("player.html", user_play_queue=users_tracks, global_play_queue=global_queue)

@app.route('/player/status/poll', methods=['GET'])
@with_mpd
def status(mpd):
    """An endpoint for poll-based player status updates."""
    client_current = request.args.get('current', None)
    if client_current is not None:
        client_current = int(client_current)

    response = _get_status(mpd)

    if client_current is None or client_current < last_updated['playlist']:
        response['global_queue'] = [track.as_dict() for track in get_global_queue()]
        response['last_global_playlist_update'] = ceil(last_updated['playlist'])
        app.logger.debug("Issuing playlist update for user %r" % session['user']['name'])

    return jsonify(response)

@app.route('/player/status/idle')
@with_mpd
def idle(mpd):
    """An endpoint for push-based player events.

    The function issues an MPD IDLE command to Mopidy and blocks on response back from Mopidy. Once a response is received, a Server-Sent Events (SSE) transmission is prepared
    and returned as the response to the request."""
    mpd.send_idle()
    select.select([mpd], [], [])
    changed = mpd.fetch_idle()
    status = _get_status(mpd)
    event = "event: %s\ndata: %s" % (changed[0], json.dumps(status))
    app.logger.debug(event)
    return Response(event, mimetype='text/event-stream', direct_passthrough=True)

def get_global_queue():
    return PlayQueueEntry.query.order_by(PlayQueueEntry.playback_priority).all()

def get_user_queue(user):
    return PlayQueueEntry.query.filter(PlayQueueEntry.user_id == user)

def _get_status(mpd):
    """Get the entire player status needed for the front end."""
    # Get the player status
    player_status = mpd.status()
    # Get the current song
    current_song = mpd.currentsong()

    status = {}
    for key in ('title', 'artist', 'album', 'date', 'file', 'time', 'id'):
        status[key] = current_song.get(key, 0 if key == 'time' else '')
    for key in ('state', 'volume', 'elapsed'):
        status[key] = player_status.get(key, 0 if key == 'elapsed' else '')

    # Throw in a timestamp to assist synchronization
    status['response_time'] = time.time()

    return status