import time
from multiprocessing import Manager, Process

from flask import Flask, jsonify, redirect, session, url_for

app = Flask("partify")

from partify.config import load_config_from_db
from partify.queue import on_playlist_update, ensure_mpd_playlist_consistency

@app.route("/")
def main():
    """The 'default' route when you hit the index of the app.
    Just sweeps the user off to the player page (which redirects to login if there is no user authenticated)."""
    return redirect(url_for('player'))

def on_startup():
    load_config_from_db()
    ipc.init_times()
    ensure_mpd_playlist_consistency()
    ipc.update_time('playlist', time.time())

    # Start the process which subscribes to MPD events using the IDLE command
    mpd_event_listener = Process(target=on_playlist_update)
    mpd_event_listener.start()
