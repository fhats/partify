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
from partify.priv import dump_user_privileges, user_has_privilege

@app.route('/player', methods=['GET'])
@with_authentication
def player():
    """Display the player page.

    Sends the user's queue and the global queue along and displays the player page."""
    users_tracks = get_user_queue(session['user']['id'])
    global_queue = get_global_queue()

    config = {'lastfm_api_key': app.config['LASTFM_API_KEY'], 'lastfm_api_secret': app.config['LASTFM_API_SECRET']}

    user = User.query.get(session['user']['id'])

    # Do some logic to figure out if we need to show the admin console (i.e. the hostname or port for the MPD server are blank)
    if app.config['MPD_SERVER_HOSTNAME'] == "" or app.config['MPD_SERVER_PORT'] == "":
        if user_has_privilege(user, "ADMIN_INTERFACE") and user_has_privilege(user, "ADMIN_CONFIG"):
            return redirect(url_for("admin_console"))

    return render_template("player.html", user=user, user_play_queue=users_tracks, global_play_queue=global_queue, config=config, user_privs=dump_user_privileges(user))

@app.route('/player/status/poll', methods=['GET'])
@with_authentication
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
        response['last_global_playlist_update'] = playlist_last_updated
    else:
        del response['elapsed']

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
    for key in ('state', 'volume', 'elapsed', 'consume', 'random', 'repeat', 'single'):
        status[key] = player_status.get(key, 0 if key == 'elapsed' else '')

    # Throw in a timestamp to assist synchronization
    status['response_time'] = time.time()

    return status