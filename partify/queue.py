"""This file provides endpoints for queue management as well as queue-related algorithms and internal management."""
import json
import logging
import select
import time
import urllib2
from itertools import izip_longest

from flask import jsonify, redirect, request, session, url_for
from sqlalchemy import not_
from sqlalchemy.event import listens_for

from database import db_session
from decorators import with_authentication
from decorators import with_mpd
from partify import app, last_updated
from partify.models import PlayQueueEntry
from partify.models import Track
from partify.player import _get_status

@app.route('/queue/add', methods=['POST'])
@with_authentication
@with_mpd
def add_to_queue(mpd):
    """Takes a Spotify URL and adds it to the current play queue."""

    spotify_uri = request.form['spotify_uri']
    
    track = track_from_spotify_url(spotify_uri)
    
    # This search is here to help mitigate the issue with Spotify metadata loading slowly in Mopidy
    mpd.search('filename', spotify_uri)
    
    mpd_id = mpd.addid(spotify_uri)

    # Add the track to the play queue
    db_session.add( PlayQueueEntry(track=track, user_id=session['user']['id'], mpd_id=mpd_id) )
    db_session.commit()

    _ensure_mpd_playlist_consistency(mpd)

    return jsonify(status='ok', file=spotify_uri)

@app.route('/queue/remove', methods=['POST', 'GET'])
@with_authentication
@with_mpd
def remove_from_queue(mpd):
    track_id = request.form.get('track_id', None)
    track_id = request.args.get('track_id', None)

    if track_id is None:
        return jsonify(status='error', message="No track specified for removal!")
    
    track_id = int(track_id)

    # Pull the track from the play queue
    track = PlayQueueEntry.query.filter(PlayQueueEntry.mpd_id == track_id).first()
    if track is None:
        return jsonify(status='error', message="Could not find track with id %d" % track_id)

    if track.user.id != session['user']['id']:
        return jsonify(status='error', message="You are not authorized to remove this track!")
    
    # Remove the track! All of the details will follow for now.... later we'll need to be watching the reordering of tracks (#20)
    mpd.deleteid(track_id)

    return jsonify(status='ok')


def track_from_spotify_url(spotify_url):
    """Returns a Track object from the Spotify metadata associated with the given Spotify URI."""
    existing_tracks = Track.query.filter(Track.spotify_url == spotify_url).all()

    if len(existing_tracks) == 0:
        # If we have a track that does not already have a Track entry with the same spotify URI, then we need get the information from Spotify and add one.
        
        # Look up the info from the Spotify metadata API
        track_info = track_info_from_spotify_url(spotify_url)

        track = Track(**track_info)
        db_session.add( track )
        db_session.commit()
    else:
        track = existing_tracks[0]

    return track

def track_info_from_spotify_url(spotify_url):
    """Returns track information from the Spotify metadata API from the given Spotify URI."""
    spotify_request_url = "http://ws.spotify.com/lookup/1/.json?uri=%s" % spotify_url
    raw_response = urllib2.urlopen(spotify_request_url).read()

    response = json.loads(raw_response)

    # TODO: When this becomes a JSON response, chain together dict references using .get and check for Nones at the end
    track_info = {
        'title': response['track']['name'],
        'artist': ', '.join(artist['name'] for artist in response['track']['artists']),
        'album': response['track']['album']['name'],
        'spotify_url': spotify_url,
        'date': raw_info_from_spotify_url(response['track']['album']['href'])['album']['released']
    }

    return track_info

def raw_info_from_spotify_url(spotify_url):
    spotify_request_url = "http://ws.spotify.com/lookup/1/.json?uri=%s" % spotify_url
    raw_response = urllib2.urlopen(spotify_request_url).read()

    response = json.loads(raw_response)

    return response

@with_mpd
def ensure_mpd_playlist_consistency(mpd):
    """A wrapper for _ensure_mpd_playlist_consistency that grabs an MPD client."""
    _ensure_mpd_playlist_consistency(mpd)

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
        db_session.delete(purge_entry)
    db_session.commit()

    for track in playlist_tracks:
        # This could cause some undue load on the database. We can do this in memory if it's too intensive to be doing DB calls
        queue_track = PlayQueueEntry.query.filter(PlayQueueEntry.mpd_id == track['id']).first() # Don't need to worry about dups since this field is unique in the DB

        if queue_track is not None:
            # Do some checking here to make sure that all of the information is correct...
            queue_track.playback_priority = track['pos']
        else:
            # We need to add the track to the Partify representation of the Play Queue
            new_track = track_from_spotify_url(track['file'])
            new_track_entry = PlayQueueEntry(track=new_track, user_id=None, mpd_id=track['id'], playback_priority=track['pos'])
            db_session.add(new_track_entry)

    db_session.commit()

    status = _get_status(mpd)
    if status['state'] != 'play':
        mpd.play()

@with_mpd
def on_playlist_update(mpd, last_updated_dict):
    """The subprocess that continuously IDLEs against the Mopidy server and ensures playlist consistency on playlist update."""
    while True:
        changed = mpd.idle()
        app.logger.debug("Received change event from Mopidy: %s" % changed)
        if changed[0] == 'playlist':
            _ensure_mpd_playlist_consistency(mpd)

        # Update the dict which assists caching
        for changed_system in changed:
            last_updated_dict[changed_system] = time.time()
            app.logger.debug(last_updated_dict)
