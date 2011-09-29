import time
from multiprocessing import Process

from werkzeug.serving import run_simple

from partify import app, last_updated
from partify.queue import on_playlist_update, ensure_mpd_playlist_consistency

from partify import player, queue, track, user

if __name__ == "__main__":
    """Starts the WebApp."""

    ensure_mpd_playlist_consistency()
    last_updated['playlist'] = time.time()

    # Start the process which subscribes to MPD events using the IDLE command
    mpd_event_listener = Process(target=on_playlist_update, args=(last_updated,))
    mpd_event_listener.start()

    app.run(debug=True)