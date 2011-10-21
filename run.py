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
    if app.config['SERVER'] == 'builtin':
        app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'], debug=False)
    elif app.config['SERVER'] == 'tornado':
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop

        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(app.config['SERVER_PORT'])
        IOLoop.instance().start()