"""This file provides endpoints for queue management as well as queue-related algorithms and internal management."""
import json
import logging
import urllib2

from flask import redirect, request, session, url_for

from database import db_session
from decorators import with_authentication
from decorators import with_mpd
from partify import app
from partify.models import PlayQueueEntry
from partify.models import Track

@app.route('/queue/add', methods=['POST'])
@with_authentication
def add_to_queue():
    """For right now, just take a spotfy URL and add the track to the play queue..."""

    spotify_uri = request.form['spotify_uri']
    existing_tracks = Track.query.filter(Track.spotify_url == spotify_uri).all()

    if len(existing_tracks) == 0:
        # If we have a track that does not already have a Track entry with the same spotify URI, then we need get the information from Spotify and add one.
        
        # Look up the info from the Spotify metadata API
        spotify_request_url = "http://ws.spotify.com/lookup/1/.json?uri=%s" % spotify_uri
        raw_response = urllib2.urlopen(spotify_request_url).read()

        response = json.loads(raw_response)

        # TODO: When this becomes a JSON response, chain together dict references using .get and check for Nones at the end
        track_info = {
            'title': response['track']['name'],
            'artist': ', '.join(artist['name'] for artist in response['track']['artists']),
            'album': response['track']['album']['name']
        }
        track = Track(**track_info)
        db_session.add( track )
    else:
        track = existing_tracks[0]
    
    # Add the track to the play queue
    db_session.add( PlayQueueEntry(track=track, user_id=session['user']['id']) )
    db_session.commit()

    return redirect(url_for('player'))

def _ensure_mpd_playlist_consistency():
    """I think this will go here...?"""
    pass