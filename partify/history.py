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

import datetime
from math import ceil

from flask import jsonify, request

from partify import app
from partify.models import PlayHistoryEntry

@app.route("/history", methods=['GET'])
def history():
    """Returns a JSON structure representing the track history for a period specified by the client.

    If ipp is specified, the return value is at most ipp items long. If page is specified, then ipp items are shown starting at page page.
    ipp defaults to 25, page defaults to 1."""

    ipp = request.args.get('ipp', 25)
    ipp = int(ipp)
    page = request.args.get('page', 1)
    page = int(page)

    # Get some meta information about the page and how many results came back...
    total_entries = PlayHistoryEntry.query.count()
    total_pages = ceil(total_entries / float(ipp))

    if (page > total_pages and total_pages > 0) or page < 1:
        return jsonify(status='error', message='You requested a page that does not exist!')

    history_slice = PlayHistoryEntry.query.order_by(PlayHistoryEntry.time_played.desc()).offset(ipp * (page-1)).limit(ipp).all()

    result_history = []

    # Format each track to send back only the data we want...
    for entry in history_slice:
        track = entry.track
        user = entry.user
        time_played = entry.time_played
        history_entry = {
            "id": entry.id,
            "title": track.title,
            "artist": track.artist,
            "album": track.album,
            "length": track.length,
            "date": track.date,
            "user": user.name,
            "time_played": time_played.isoformat(),
        }
        result_history.append(history_entry)

    return jsonify(status='ok', tracks=result_history, num_items=len(result_history), page=page, pages=int(total_pages), response_time=(datetime.datetime.now()).isoformat())