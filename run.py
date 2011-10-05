import time
from multiprocessing import Manager, Process

from werkzeug.serving import run_simple

import partify
from config import SERVER_HOST, SERVER_PORT
from partify import app
from partify.queue import on_playlist_update, ensure_mpd_playlist_consistency

from partify import player, queue, track, user

if __name__ == "__main__":
    """Starts the WebApp."""
    manager = Manager()
    partify.last_updated = manager.dict()
    ensure_mpd_playlist_consistency()
    partify.last_updated['playlist'] = time.time()

    # Start the process which subscribes to MPD events using the IDLE command
    mpd_event_listener = Process(target=on_playlist_update, args=(partify.last_updated,manager))
    mpd_event_listener.start()

    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)