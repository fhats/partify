from werkzeug.serving import run_simple

from partify import app
from partify import ipc
from partify import on_startup

# TODO: Figure out these imports
from partify import player, queue, track, user

if __name__ == "__main__":
    """Starts the WebApp."""
    app.logger.debug(app.config)

    on_startup()

    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'], debug=False)