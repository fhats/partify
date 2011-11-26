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

from datetime import datetime
from datetime import timedelta
import operator

from flask import jsonify

from partify import app
from partify.models import PlayHistoryEntry
from partify.models import Track

@app.route("/statistics", methods=['GET'])
def statistics():
    # TODO: At some point, allow for statistics to be requested by key
    # For now, just dump a bunch of stats back out

    stats = {
        "all": {},
        "year": {},
        "month": {},
        "week": {},
        "day": {}
    }

    # compute some datetime segments to form the boundaries for statistics computations
    current_time = datetime.now()
    boundaries = {
        "all": datetime.min,
        "year": current_time - timedelta(days=+365),
        "month": current_time - timedelta(days=+30),
        "week": current_time - timedelta(weeks=+1),
        "day": current_time - timedelta(days=+1)
    }

    for key, boundary in boundaries.iteritems():
        # Grab the segment of history from the database
        segment = PlayHistoryEntry.query.filter(PlayHistoryEntry.time_played > boundary).all()
        stats[key] = compute_stats_over_segment(segment)
    
    return jsonify(status="ok", statistics=stats, response_time=(datetime.now()).isoformat())

def compute_stats_over_segment(segment):
    """Computes some statistics over a segment of history.

    Note that this could be pretty slow to start. May be worth finding a way to speed this up eventually."""
    stats = {}

    stats["total_tracks"] = len(segment)
    
    # Compute the most played artists in this segment
    artists = {}
    for entry in segment:
        artist = entry.track.artist
        if artist in artists:
            artists[artist] += 1
        else:
            artists[artist] = 1
    
    artists = sorted(artists.iteritems(), key=operator.itemgetter(1), reverse=True)
    if len(artists) > 0:
        artists = artists[:min(4    , len(artists))]
        stats["top_artists"] = {}
        rank = 1
        for artist, plays in artists:
            stats["top_artists"][rank] = {"artist": artist, "plays": plays}
            rank += 1

    # Compute the most played albums in this segment
    albums = {}
    album_artists = {}
    for entry in segment:
        album = entry.track.album
        if album in albums:
            albums[album] += 1
        else:
            albums[album] = 1
            album_artists[album] = entry.track.artist
    
    albums = sorted(albums.iteritems(), key=operator.itemgetter(1), reverse=True)
    if len(albums) > 0:
        albums = albums[:min(4, len(albums))]
        stats["top_albums"] = {}
        rank = 1
        for album, plays in albums:
            stats["top_albums"][rank] = {"album": album, "plays": plays, "artist": album_artists[album]}
            rank += 1

    # Compute the users with the most plays
    users = {}
    username_to_display_name = {}
    for entry in segment:
        user = entry.user.username
        if user in users:
            users[user] += 1
        else:
            users[user] = 1
            username_to_display_name[user] = entry.user.name

    users = sorted(users.iteritems(), key=operator.itemgetter(1), reverse=True)
    if len(users) > 0:
        users = users[:min(4, len(users))]
        stats["top_users"] = {}
        rank = 1
        for user, plays in users:
            stats["top_users"][rank] = {"user": username_to_display_name[user], "plays": plays, "username": user}
            rank += 1

    stats["total_time"] = sum( [entry.track.length for entry in segment] )

    return stats