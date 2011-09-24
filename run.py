from multiprocessing import Process

from werkzeug.serving import run_simple

from partify import app
from partify.queue import on_playlist_update

from partify import player, queue, track, user

if __name__ == "__main__":
    """Starts the WebApp."""

    # Start the process which subscribes to MPD events using the IDLE command
    mpd_event_listener = Process(target=on_playlist_update)
    mpd_event_listener.start()

    app.run(debug=True)