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
import json
import random

from testify import *

from partify import app
from partify import history
from partify.database import db
from partify.models import PlayHistoryEntry
from partify.queue import track_from_spotify_url
from testing.data.sample_tracks import sample_tracks
from testing.partify_test_case import PartifyTestCase

class HistoryTestCase(PartifyTestCase):

    @class_setup
    def add_tracks(self):
        self.user = self.create_test_user()
        self.added_tracks = []
        r = random.Random()
        for i in range(1,100):
            sample_track = r.choice(sample_tracks)
            track_to_add = track_from_spotify_url(sample_track['file'])
            self.added_tracks.append(track_to_add)
            when = datetime.datetime(datetime.MINYEAR, 1, 1, 0, 0, 0, i)
            phe = PlayHistoryEntry(track=track_to_add, user=self.user, time_played=when)
            db.session.add(phe)
        db.session.commit()

    def test_endpoint_works(self):
        response = self.assert_endpoint_works("/history")
        rdata = json.loads(response.data)
        assert rdata['status'] == 'ok'

    def test_contents(self):
        expected_tracks = reversed(self.added_tracks)

        response = self.assert_endpoint_works("/history")
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['num_items'] == 25
        assert response['page'] == 1
        assert response['pages'] == 4

        for response_track, expected_track in zip(response['tracks'], expected_tracks):
            assert response_track['title'] == expected_track.title
            assert response_track['artist'] == expected_track.artist
            assert response_track['album'] == expected_track.album
            assert response_track['length'] == expected_track.length
            assert response_track['user'] == self.user.name
            
    def test_paging(self):
        response = self.assert_endpoint_works("/history")
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['page'] == 1
        assert response['pages'] == 4
        first_page_tracks = response['tracks']
        
        response = self.assert_endpoint_works("/history?page=4")
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['page'] == 4
        assert response['pages'] == 4
        assert response['tracks'] != first_page_tracks

        response = self.assert_endpoint_works("/history?page=6")
        response = json.loads(response.data)
        assert response['status'] != 'ok'
        assert response['status'] == 'error'

        response = self.assert_endpoint_works("/history?page=0")
        response = json.loads(response.data)
        assert response['status'] != 'ok'
        assert response['status'] == 'error'
    
    def test_items_per_page(self):
        response = self.assert_endpoint_works("/history")
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['num_items'] == 25
        assert response['pages'] == 4
        first_page_tracks = response['tracks']

        response = self.assert_endpoint_works("/history?ipp=50")
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['num_items'] == 50
        assert response['pages'] == 2
        assert response['tracks'] != first_page_tracks

        response = self.assert_endpoint_works("/history?ipp=10&page=10")
        response = json.loads(response.data)
        assert response['status'] == 'ok'
        assert response['num_items'] == 9
        assert response['pages'] == 10
        assert response['tracks'] != first_page_tracks



