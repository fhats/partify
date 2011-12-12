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

import json
import random

from testify import *

from partify import app
from partify import vote
from partify.database import db
from partify.models import PlayQueueEntry, Vote
from partify.queue import track_from_spotify_url
from testing.data.sample_tracks import sample_tracks
from testing.logged_in_user_test_case import LoggedInUserTestCase

class VoteTestCase(LoggedInUserTestCase):
    @setup
    def setup_track(self):
        self.user_id = self.user.id
        self.queueing_user = self.create_test_user()
        self.queueing_user_id = self.queueing_user.id
        r = random.Random()
        st = r.choice(sample_tracks)
        track = track_from_spotify_url(st['file'])
        self.pqe = PlayQueueEntry(track = track, user=self.queueing_user)
        db.session.add(self.pqe)
        db.session.commit()

    def test_vote_status(self):
        response = self.assert_endpoint_works('/vote/status?pqe=%d' % self.pqe.id)
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['direction'] == 0

        self.pqe.user_id = self.user_id

        db.session.add(self.pqe)
        db.session.commit()

        response = self.assert_endpoint_works('/vote/status?pqe=%d' % self.pqe.id)
        response = json.loads(response.data)
        assert response['status'] == 'error'

        self.pqe.user_id = self.queueing_user_id
        db.session.add(self.pqe)
        v = Vote(pqe=self.pqe, user=self.user, direction = 1)
        db.session.add(v)
        db.session.commit()

        response = self.assert_endpoint_works('/vote/status?pqe=%d' % self.pqe.id)
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['direction'] == 1

    def test_vote_up(self):
        pqe_id = self.pqe.id
        self.pqe.user_id = self.user_id

        db.session.add(self.pqe)
        db.session.commit()

        response = self.app.post('/vote/up', data={'pqe': self.pqe.id})
        assert response.status_code == 200
        response = json.loads(response.data)
        assert response['status'] == 'error'

        self.pqe.user_id = self.queueing_user_id
        db.session.add(self.pqe)
        db.session.commit()

        response = self.app.post('/vote/up', data={'pqe': self.pqe.id})
        assert response.status_code == 200
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        votes = Vote.query.filter(db.and_(Vote.pqe_id == pqe_id, Vote.user_id == self.user_id)).all()
        assert len(votes) == 1
        assert votes[0].direction == 1

    def test_vote_down(self):
        pqe_id = self.pqe.id
        self.pqe.user_id = self.user_id

        db.session.add(self.pqe)
        db.session.commit()

        response = self.app.post('/vote/down', data={'pqe': self.pqe.id})
        assert response.status_code == 200
        response = json.loads(response.data)
        assert response['status'] == 'error'

        self.pqe.user_id = self.queueing_user_id
        db.session.add(self.pqe)
        db.session.commit()

        response = self.app.post('/vote/down', data={'pqe': self.pqe.id})
        assert response.status_code == 200
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        votes = Vote.query.filter(db.and_(Vote.pqe_id == pqe_id, Vote.user_id == self.user_id)).all()
        assert len(votes) == 1
        assert votes[0].direction == -1

    def test_vote_total(self):
        pqe_id = self.pqe.id
        target_sum = 0
        r = random.Random()
        for i in range(1,51):
            direction = r.choice([-1, 0,1])
            target_sum += direction
            user = self.create_test_user()
            v = Vote(pqe=self.pqe, user=user, direction=direction)
            db.session.add(v)
        db.session.commit()

        response = self.assert_endpoint_works("/vote/total?pqe=%d" % pqe_id)
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['total'] == target_sum
