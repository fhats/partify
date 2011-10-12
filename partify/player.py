import json
import random
import select
import time
from math import ceil

from flask import Response, jsonify, redirect, render_template, request, session, url_for

from decorators import with_authentication, with_mpd
from partify import app
from partify import ipc
from partify.models import PlayQueueEntry
from partify.models import Track
from partify.models import User

@app.route('/player', methods=['GET'])
@with_authentication
def player():
    """Display the player page.

    Sends the user's queue and the global queue along and displays the player page."""
    users_tracks = get_user_queue(session['user']['id'])
    global_queue = get_global_queue()

    return render_template("player.html", user=User.query.get(session['user']['id']), user_play_queue=users_tracks, global_play_queue=global_queue)

@app.route('/player/status/poll', methods=['GET'])
@with_mpd
def status(mpd):
    """An endpoint for poll-based player status updates."""
    client_current = request.args.get('current', None)
    if client_current is not None:
        client_current = float(client_current)

    response = _get_status(mpd)

    playlist_last_updated = ipc.get_time('playlist')
    if client_current is None or client_current < playlist_last_updated:
        response['global_queue'] = get_global_queue()
        response['user_queue'] = get_user_queue(session['user']['id'])
        response['last_global_playlist_update'] = ceil(playlist_last_updated)

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
    db_queue = PlayQueueEntry.query.order_by(PlayQueueEntry.playback_priority).all()
    return [track.as_dict() for track in db_queue]

def get_user_queue(user):
    db_queue = PlayQueueEntry.query.filter(PlayQueueEntry.user_id == user).order_by(PlayQueueEntry.user_priority)
    return [track.as_dict() for track in db_queue]

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