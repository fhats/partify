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

"""A collection of endpoints used for debugging the application. Each of these controls an aspect of playback."""

from decorators import default_json
from decorators import with_mpd
from mpd_client import mpd_client
from partify import app

@app.route('/playback/play')
@default_json
@with_mpd
def play(mpd):
    return mpd.play()

@app.route('/playback/pause')
@default_json
@with_mpd
def pause(mpd):
    app.logger.debug("Pausing")
    return mpd.pause()

@app.route('/playback/next')
@default_json
@with_mpd
def next(mpd):
    app.logger.debug("Skipping to next track.")
    return mpd.next()

@app.route('/playback/prev')
@default_json
@with_mpd
def prev(mpd):
    app.logger.debug("Going back to previous track.")
    return mpd.previous()