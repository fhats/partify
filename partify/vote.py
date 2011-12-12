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

"""A collection of endpoints for voting on tracks and getting voting
information."""

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
    """Gets the logged-in user's vote status for a certain track.

    :param pqe: The ID of the :class:`~partify.models.PlayQueueEntry`
    :type pqe: integer
    :returns: The status of the request and the direction of any existing vote.
    :rtype: JSON string 
    """
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
    """Records a vote in the up direction for the logged-in user.
    
    :param pqe: The ID of the :class:`~partify.models.PlayQueueEntry`
    :type pqe: integer
    :returns: The status of the request.
    :rtype: JSON string 
    """
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
    """Records a vote in the down direction for the logged-in user.

    :param pqe: The ID of the :class:`~partify.models.PlayQueueEntry`
    :type pqe: integer
    :returns: The status of the request.
    :rtype: JSON string 
    """
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
    """Retreives the total vote score for the specified track. One of pqe or phe must be 
    specified, but not both.

    :param pqe: The ID of the :class:`~partify.models.PlayQueueEntry`
    :type pqe: integer, optional
    :param phe: The ID of the :class:`~partify.models.PlayHistoryEntry`
    :type phe: integer, optional
    :returns: The status of the request and the total vote score of the specified track.
    :rtype: JSON string
    """

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
