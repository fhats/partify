"""Copyright 2011 Fred Hatfull

This file is part of Partify.

Partify is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Partify is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Partify.  If not, see <http://www.gnu.org/licenses/>."""

from werkzeug.serving import run_simple

from partify import app
from partify import ipc
from partify import on_startup

# TODO: Figure out these imports
from partify import player, queue, track, user

if __name__ == "__main__":
    """Starts the WebApp."""
    on_startup()
    
    app.logger.debug(app.config)

    if app.config['SERVER'] == 'builtin':
        app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
    elif app.config['SERVER'] == 'tornado':
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop

        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(app.config['SERVER_PORT'])
        IOLoop.instance().start()