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

"""This file provides endpoints for queue management as well as queue-related algorithms and internal management."""
import itertools
import json
import logging
import select
import time
import urllib2
from itertools import izip_longest
from urllib2 import HTTPError

from flask import jsonify, redirect, request, session, url_for
from sqlalchemy import and_, func, not_
from sqlalchemy.event import listens_for

from database import db
from decorators import with_authentication
from decorators import with_mpd
from decorators import with_mpd_lock
from partify import app
from partify import ipc
from partify.models import PlayQueueEntry
from partify.models import Track
from partify.models import User
from partify.player import get_user_queue, _get_status

@app.route('/queue/add', methods=['POST'])
@with_authentication
@with_mpd
@with_mpd_lock
def add_to_queue(mpd):
    """Takes a Spotify URL and adds it to the current play queue."""

    spotify_uri = request.form['spotify_uri']
    
    track = track_from_spotify_url(spotify_uri)

    if track is None:
        return jsonify(status='error', message='The Spotify URL you specified is invalid.')
    
    mpd_id = mpd.addid(spotify_uri)

    # Add the track to the play queue
    # Disabling this for now since the playlist consistency function should figure it out
    db.session.add( PlayQueueEntry(track=track, user_id=session['user']['id'], mpd_id=mpd_id) )
    db.session.commit()

    return jsonify(status='ok', queue=get_user_queue(session['user']['id']), file=spotify_uri)

@app.route('/queue/remove', methods=['POST'])
@with_authentication
@with_mpd
@with_mpd_lock
def remove_from_queue(mpd):
    track_id = request.form.get('track_id', None)

    if track_id is None:
        return jsonify(status='error', message="No track specified for removal!")
    
    try:
        track_id = int(track_id)
    except ValueError:
        return jsonify(status='error', message="Not a valid track ID!")

    # Pull the track from the play queue
    track = PlayQueueEntry.query.filter(PlayQueueEntry.mpd_id == track_id).first()
    if track is None:
        return jsonify(status='error', message="Could not find track with id %d" % track_id)

    if track.user.id != session['user']['id']:
        return jsonify(status='error', message="You are not authorized to remove this track!")
    
    # Remove the track! All of the details will follow for now.... later we'll need to be watching the reordering of tracks (#20)
    mpd.deleteid(track_id)

    return jsonify(status='ok', queue=get_user_queue(session['user']['id']))

@app.route('/queue/reorder', methods=['POST'])
@with_authentication
def reorder_queue():
    """Reorders the user's play queue.

    I *think* for right now this can essentially take a list of PlayQueueEntry IDs and new priorities and write to the DB.
    I guess then track order ends up being ensured as part of the consistency function...? In which case the first comment is no longer true."""
    # I think this logic will probably change based on plug-and-play queue management schemes...

    new_order_list = request.form.get('track_list')

    # expecting a dictionary of request parameters with the key as the PQE id and the value as the new priority
    # Note that I'm not doing any error checking here because 500ing is good enough right now
    # Should probably put a try...catch block around the cast to int
    for pqe_id, new_priority in request.form.iteritems():
        pqe = PlayQueueEntry.query.get(pqe_id)

        # TODO: This auth checking should move into its own function!
        if pqe.user.id != session['user']['id']:
            return jsonify(status='error', message="You are not authorized to modify this track!")

        pqe.user_priority = new_priority

        db.session.commit()

    ensure_mpd_playlist_consistency()

    # TODO: This returning the queue thing should probably get moved to a decorator or something
    return jsonify(status='ok', queue=get_user_queue(session['user']['id']))

@app.route('/queue/list', methods=['GET'])
@with_authentication
def list_user_queue():
    user_queue = get_user_queue(session['user']['id'])
    return jsonify(status="ok", result=user_queue)

# These *_from_spotify_url functions should probably move to a kind of util file
def track_from_spotify_url(spotify_url):
    """Returns a Track object from the Spotify metadata associated with the given Spotify URI."""
    existing_tracks = Track.query.filter(Track.spotify_url == spotify_url).all()

    if len(existing_tracks) == 0:
        # If we have a track that does not already have a Track entry with the same spotify URI, then we need get the information from Spotify and add one.
        
        # Look up the info from the Spotify metadata API
        track_info = track_info_from_spotify_url(spotify_url)
        if track_info is None:
            return None

        track = Track(**track_info)
        db.session.add( track )
        db.session.commit()
    else:
        track = existing_tracks[0]

    return track

def track_from_mpd_search_results(spotify_url, mpd):
    existing_tracks = Track.query.filter(Track.spotify_url == spotify_url).all()

    if len(existing_tracks) == 0:
        track_info = track_info_from_mpd_search_results(spotify_url, mpd)
        if track_info is None:
            return None
        
        track = Track(**track_info)
        db.session.add( track )
        db.session.commit()
    else:
        track = existing_tracks[0]

    return track


def track_info_from_mpd_search_results(spotify_url, mpd):
    results = mpd.search('filename', spotify_url)

    result = results[0]

    track_info = {
        'title': result['title'],
        'artist': result['artist'],
        'album': result['album'],
        'spotify_url': result['file'],
        'date': result['date'],
        'length': result['time']
    }

    return track_info

def track_info_from_spotify_url(spotify_url):
    """Returns track information from the Spotify metadata API from the given Spotify URI."""
    spotify_request_url = "http://ws.spotify.com/lookup/1/.json?uri=%s" % spotify_url
    
    try:
        raw_response = urllib2.urlopen(spotify_request_url).read()
    except HTTPError:
        return None

    response = json.loads(raw_response)

    # TODO: When this becomes a JSON response, chain together dict references using .get and check for Nones at the end
    track_info = {
        'title': response['track']['name'],
        'artist': ', '.join(artist['name'] for artist in response['track']['artists']),
        'album': response['track']['album']['name'],
        'spotify_url': spotify_url,
        'date': _raw_info_from_spotify_url(response['track']['album']['href'])['album']['released'],
        'length': response['track']['length']
    }

    return track_info

def _raw_info_from_spotify_url(spotify_url):
    spotify_request_url = "http://ws.spotify.com/lookup/1/.json?uri=%s" % spotify_url
    raw_response = urllib2.urlopen(spotify_request_url).read()

    response = json.loads(raw_response)

    return response

def _get_users_next_pqe_entry_after_playback_priority(user_id, playback_priority):
    return PlayQueueEntry.query.filter(and_(PlayQueueEntry.user_id == user_id, PlayQueueEntry.playback_priority > playback_priority)).order_by(PlayQueueEntry.user_priority.asc()).first()

@with_mpd
def ensure_mpd_playlist_consistency(mpd):
    """A wrapper for _ensure_mpd_playlist_consistency that grabs an MPD client."""
    _ensure_mpd_playlist_consistency(mpd)

@with_mpd_lock
def _ensure_mpd_playlist_consistency(mpd):
    """Responsible for ensuring that the Partify play queue database table is in sync with the Mopidy play queue.

    This function should ensure consistency according to the following criteria:
    * The Mopidy playlist is authoritative.
    * The function should be lightweight and should not make undue modifications to the database.
    """
    playlist_tracks = mpd.playlistinfo()
    playlist_ids = [track['id'] for track in playlist_tracks]
    
    # Purge all the database entries that don't have IDs present
    purge_entries = PlayQueueEntry.query.filter(not_(PlayQueueEntry.mpd_id.in_(playlist_ids))).all()
    for purge_entry in purge_entries:
        db.session.delete(purge_entry)
        app.logger.debug("Removing Play Queue Entry %r" % purge_entry)
    db.session.commit()

    for track in playlist_tracks:
        # This could cause some undue load on the database. We can do this in memory if it's too intensive to be doing DB calls
        queue_track = PlayQueueEntry.query.filter(PlayQueueEntry.mpd_id == track['id']).first() # Don't need to worry about dups since this field is unique in the DB

        if queue_track is not None:
            # Do some checking here to make sure that all of the information is correct...
            # Ensure that the playback position is correct
            queue_track.playback_priority = track['pos']
        else:
            # We need to add the track to the Partify representation of the Play Queue
            new_track = track_from_spotify_url(track['file'])
            new_track_entry = PlayQueueEntry(track=new_track, user_id=None, mpd_id=track['id'], playback_priority=track['pos'])
            db.session.add(new_track_entry)

    db.session.commit()

    # Ensure that the playlist's order follows a selection method - in this case, round robin.
    # This should *probably* move to its own function later... for now this is just research!
    # A rough idea of the implemention of round-robin ordering can be found in issue #20 (https://github.com/fxh32/partify/issues/20)

    # Before we do anything else we need the track list from the DB
    db_tracks = PlayQueueEntry.query.order_by(PlayQueueEntry.playback_priority.asc()).all()

    if len(db_tracks) > 0:

        # First, grab a list of all users that currently have PlayQueueEntrys (we can interpret this as active users)
        # TODO: This is dumb and slow and can be improved by doing a better DB query. Right now I'm just avoiding learning how to do this query with the ORM (if it can be done).
        users = set([pqe.user for pqe in PlayQueueEntry.query.all()])
        unique_users = users = sorted(users, key=lambda d: getattr(d, 'username', 'anonymous'))
        # Turn the sorted user list into a cycle for repeated iteration
        users = itertools.cycle(users)
        current_user = (PlayQueueEntry.query.order_by(PlayQueueEntry.playback_priority.asc()).first()).user

        # Advance the user list to the current user
        users = itertools.dropwhile(lambda x: x != current_user, users)

        user_list = []
        user_counts = dict( (user, PlayQueueEntry.query.filter(PlayQueueEntry.user == user).count()) for user in unique_users )

        # generate a list of users to zip against the track list
        for user in users:
            if all( [user_count == 0 for user_count in user_counts.itervalues()] ):
                break
            
            if user_counts[user] > 0:
                user_counts[user] -= 1
                user_list.append(user)
    
        # Without a multiprocessing primitive this loop is messed up. Also it seems to work quite well for a single user.... but what the hell does that even mean, anyway?
        # Only make one MPD change per call and then break, since the MPD playlist changing will trigger another consistency check which is liable to cause DB locks and timeouts and hangs and all sorts of other nasty behavior
        for (track,user) in zip(db_tracks, user_list):
            # Check to make sure the next track's user matches the user being looked at.
            # If it doesn't, reorder to move that user's track to this position
            # Otherwise, continue onward 'cause everything cool!
            if track.user == user:
                # all that needs to happen in this situation is to check to see if the current track should be the user's next (i.e. that play order is respected)
                # if it's not, then shuffle some things around until it is.
                if PlayQueueEntry.query.filter(and_(PlayQueueEntry.user == track.user, PlayQueueEntry.user_priority < track.user_priority, PlayQueueEntry.playback_priority > track.playback_priority)).count() > 0:
                    # Get the track after the current playback priority with the minimum user_priority and make that the current track
                    new_next_track = _get_users_next_pqe_entry_after_playback_priority(track.user_id, track.playback_priority)
                    if new_next_track is not None:
                        mpd.moveid(new_next_track.mpd_id, track.playback_priority)
                    break
                else:
                    # Everything's cool!
                    pass
            else:
                # Uh-oh!
                # Something isn't round robin about this.
                # To resolve this, push the rest of the tracks back and move the user's lowest pqe after the current playback_priority to the current position.
                new_next_track = _get_users_next_pqe_entry_after_playback_priority(user.id, track.playback_priority)
                if new_next_track is not None:
                    mpd.moveid(new_next_track.mpd_id, track.playback_priority)
                break

    _ensure_mpd_player_state_consistency(mpd)

    status = _get_status(mpd)
        
    if status['state'] != ipc.get_desired_player_state()[0]:
        tn_fn = getattr(mpd, ipc.get_desired_player_state()[1])
        tn_fn()
        

def _ensure_mpd_player_state_consistency(mpd):
    """Ensure that the Mopidy server's options are consistent with options that make sense for Partify."""
    ideal_player_state = {'consume': '1', 'random': '0', 'repeat': '0', 'single': '0'}
    status = _get_status(mpd)

    for option, value in ideal_player_state.iteritems():
        if status[option] != value:
            option_method = getattr(mpd, option)
            option_method(value)

@with_mpd
def on_playlist_update(mpd):
    """The subprocess that continuously IDLEs against the Mopidy server and ensures playlist consistency on playlist update."""
    while True:
        changed = mpd.idle()
        app.logger.debug("Received change event from Mopidy: %s" % changed)
        if 'playlist' in changed:
            _ensure_mpd_playlist_consistency(mpd)
        if 'options' in changed:
            _ensure_mpd_player_state_consistency(mpd)

        # Update the dict which assists caching
        for changed_system in changed:
            ipc.update_time('playlist', time.time())
            app.logger.debug(ipc.get_time('playlist'))
