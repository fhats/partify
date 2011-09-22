from multiprocessing import Process

from werkzeug.serving import run_simple

from partify import app
from partify.queue import on_playlist_update

if __name__ == "__main__":
    # Start the MPD client
    p = Process(target=on_playlist_update)
    p.start()

    # Note that for debugging multiple clients simultaneously the default Flask WSGI server won't be appropriate (especially with debug=True)
    # For testing among multiple clients it is better to use run_simple from Werkzeug....
    #app.run()
    run_simple('localhost', 5000, app, use_reloader=True, threaded=True)
