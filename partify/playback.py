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