from flask import Flask, jsonify, redirect, session, url_for

from partify.mpd_client import mpd_client
from partify.database import db_session

app = Flask("partify")
app.config.from_object("config")

@app.route("/")
def main():
    return redirect(url_for('player'))

@app.route("/cmd/<cmd>")
def exc_cmd(cmd):
    with mpd_client("ubuntu.local", 6600) as mpd:
        f = getattr(mpd, cmd)
        response = f()
        return jsonify(response=response)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# having these imports here is kind of weird and I'm not totally sure why they are needed
# they will stay here until a point when something more elegant makes itself known.

from partify import queue
from partify import playback
from partify import player
from partify import user

if __name__ == "__main__":
    app.run()