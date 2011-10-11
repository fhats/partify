from multiprocessing import Manager

from flask import Flask, jsonify, redirect, session, url_for

app = Flask("partify")
app.config.from_object("config")

from partify.database import db_session

@app.route("/")
def main():
    """The 'default' route when you hit the index of the app.
    Just sweeps the user off to the player page (which redirects to login if there is no user authenticated)."""
    return redirect(url_for('player'))

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
