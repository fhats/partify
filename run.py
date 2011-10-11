import time
from multiprocessing import Process

from werkzeug.serving import run_simple

from partify import app
from partify import ipc
from partify.queue import on_playlist_update, ensure_mpd_playlist_consistency

# TODO: Figure out these imports
from partify import player, queue, track, user

if __name__ == "__main__":
    """Starts the WebApp."""
    ipc.init_times()
    ensure_mpd_playlist_consistency()
    ipc.update_time('playlist', time.time())

    # Start the process which subscribes to MPD events using the IDLE command
    mpd_event_listener = Process(target=on_playlist_update)
    mpd_event_listener.start()

    app.logger.debug(app.config)

    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'], debug=False)