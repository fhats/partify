from flask import jsonify, request, session
from sqlalchemy import and_

from partify import app
from partify.database import db
from partify.decorators import with_authentication
from partify.models import PlayQueueEntry, Vote
from partify.queue import ensure_mpd_playlist_consistency

@app.route("/vote/status", methods=['GET'])
@with_authentication
def vote_status():
    if 'pqe' in request.args:
        pqe = PlayQueueEntry.query.get(request.args['pqe'])
        if pqe is None:
            return jsonify(status="error", message="A PQE by that ID does not exist!")
        if pqe.user_id == session['user']['id']:
            return jsonify(status="error", message="You cannot vote on your own track!")
        vote = Vote.query.filter(and_(Vote.pqe_id == request.args['pqe'], Vote.user_id == session['user']['id'])).first()
        if vote is None:
            direction = 0
        else:
            direction = vote.direction
        return jsonify(status="ok", direction=direction)
    else:
        return jsonify(status="error", message="You must specify the id of the PlayQueueEntry to get the votes for!")

@app.route("/vote/up", methods=['POST'])
@with_authentication
def vote_up():
    if 'pqe' in request.form:
        pqe = PlayQueueEntry.query.get(request.form['pqe'])
        if pqe is None:
            return jsonify(status="error", message="A PQE by that ID does not exist!")
        if pqe.user_id == session['user']['id']:
            return jsonify(status="error", message="You cannot vote on your own track!")
        vote = Vote.query.filter(and_(Vote.pqe_id == request.form['pqe'], Vote.user_id == session['user']['id'])).first()
        if vote is None:
            vote = Vote(pqe_id=request.form['pqe'], user_id=session['user']['id'], direction=1)
            db.session.add(vote)
            db.session.commit()
        vote.direction = 1
        db.session.commit()
        ensure_mpd_playlist_consistency()
        return jsonify(status="ok")
    else:
        return jsonify(status="error", message="You must specify the id of the PlayQueueEntry to vote for it!")

@app.route("/vote/down", methods=['POST'])
@with_authentication
def vote_down():
    if 'pqe' in request.form:
        pqe = PlayQueueEntry.query.get(request.form['pqe'])
        if pqe is None:
            return jsonify(status="error", message="A PQE by that ID does not exist!")
        if pqe.user_id == session['user']['id']:
            return jsonify(status="error", message="You cannot vote on your own track!")
        vote = Vote.query.filter(and_(Vote.pqe_id == request.form['pqe'], Vote.user_id == session['user']['id'])).first()
        if vote is None:
            vote = Vote(pqe_id=request.form['pqe'], user_id=session['user']['id'], direction=-1)
            db.session.add(vote)
            db.session.commit()
        vote.direction = -1
        db.session.commit()
        ensure_mpd_playlist_consistency()
        return jsonify(status="ok")
    else:
        return jsonify(status="error", message="You must specify the id of the PlayQueueEntry to vote for it!")

@app.route("/vote/total", methods=['GET'])
def vote_total():
    if 'pqe' in request.args:
        pqe = PlayQueueEntry.query.get(request.args['pqe'])
        if pqe is None:
            return jsonify(status="error", message="A PQE by that ID does not exist!")
        total = sum([v.direction for v in Vote.query.filter(Vote.pqe_id == request.args['pqe']).all()])
        return jsonify(status="ok", total=total)
    elif 'phe' in request.args:
        phe = PlayHistoryEntry.query.get(request.args['phe'])
        if phe is None:
            return jsonify(status="error", message="A PHE by that ID does not exist!")
        total = sum([v.direction for v in Vote.query.filter(Vote.phe_id == request.args['phe']).all()])
        return jsonify(status="ok", total=total)
    else:
        return jsonify(status="error", message="You must specify the id of the PlayQueueEntry to get the total for!")