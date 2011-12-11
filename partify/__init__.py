# Copyright 2011 Fred Hatfull
#
# This file is part of Partify.
#
# Partify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Partify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Partify.  If not, see <http://www.gnu.org/licenses/>.

import datetime
from functools import wraps
import time
from multiprocessing import Manager, Process

from werkzeug.contrib.profiler import MergeStream
from werkzeug.contrib.profiler import ProfilerMiddleware
from werkzeug.serving import run_simple

from flask import Flask, jsonify, redirect, session, url_for

class FlaskWithRouteDocs(Flask):
    """A subclass of Flask to allow using :route: and :methods: in docstrings, a la Sphinx."""
    def route(self, rule, **options):
        """Overrides the @app.route decorator provided by Flask. Takes the opportunity to replace
        instances of :route: or :methods: in the wrapped function's docstring with information from 
        the app.route() decorator. If :route: or :methods: are not present in the docstring at the 
        time of wrapping, then append route and methods to bottom of the docstring for nicer documentation."""
        def decorator(f):
            route_dec = super(FlaskWithRouteDocs, self).route(rule, **options)
            methods_str = ','.join(options.get('methods', ['GET']))

            if f.__doc__ is not None and ":route:" in f.__doc__:
                f.__doc__ = f.__doc__.replace(":route:", rule)
            else:
                f.__doc__ = "%s\n\n    **Route:** ``%s``" % (f.__doc__, rule)
            if f.__doc__ is not None and ":methods:" in f.__doc__:
                f.__doc__ = f.__doc__.replace(":methods:", methods_str)
            else:
                f.__doc__ = "%s\n\n    **Methods:** ``%s``" % (f.__doc__, methods_str)
            return route_dec(f)
        return decorator
        

app = FlaskWithRouteDocs("partify")

from partify.config import load_config_from_db
from partify.database import init_db
from partify.queue import on_playlist_update, ensure_mpd_playlist_consistency

@app.route("/")
def main():
    """The 'default' route when you hit the index of the app.
    Just sweeps the user off to the player page (which redirects to login if there is no user authenticated)."""
    return redirect(url_for('player'))

def on_startup():
    """Performs all of the actions needed to get the web server up and running."""
    try:
        load_config_from_db()
    except:
        init_db()
        load_config_from_db()
    ipc.init_times()
    ipc.init_desired_player_state()
    ipc.init_mpd_lock()
    ensure_mpd_playlist_consistency()
    ipc.update_time('playlist', time.time())

    # Start the process which subscribes to MPD events using the IDLE command
    if not app.config['TESTING']:
        mpd_event_listener = Process(target=on_playlist_update)
        mpd_event_listener.start()

def start():
    """Starts the WebApp."""
    # TODO: Figure out these imports
    from partify import admin, history, player, queue, statistics, track, user, vote
    init_db()
    on_startup()
    
    app.logger.debug(app.config)

    if app.config.get('PROFILE', False):
        datetime_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        f = open("tmp/profile%s.log" % datetime_string, "w")
        stream = MergeStream(f)
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, stream)

    if app.config['SERVER'] == 'builtin':
        app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
    elif app.config['SERVER'] == 'tornado':
        import tornado.options
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop

        tornado.options.enable_pretty_logging()
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(app.config['SERVER_PORT'])
        IOLoop.instance().start()

if __name__ == "__main__":
    start()
