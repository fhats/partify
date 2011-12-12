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
from partify import statistics
from partify.database import db
from partify.models import PlayHistoryEntry
from partify.queue import track_from_spotify_url
from testing.data.sample_tracks import sample_tracks
from testing.partify_test_case import PartifyTestCase

class StatisticsTestCase(PartifyTestCase):
    
    @class_setup
    def setup_tracks(self):
        self.user = self.create_test_user()

        now = datetime.datetime.now()
        day = datetime.timedelta(hours=5)
        week = datetime.timedelta(days=4)
        month = datetime.timedelta(weeks=3)
        year = datetime.timedelta(weeks=23)
        all_time = datetime.timedelta(weeks=82)

        for time_period in [day, week, month, year, all_time]:
            # Add some tracks from today
            r = random.Random()
            for i in range(1,51):
                st = r.choice(sample_tracks)
                track = track_from_spotify_url(st['file'])
                phe = PlayHistoryEntry(track=track, user=self.user, time_played=now - time_period)
                db.session.add(phe)
        db.session.commit()    
                
    def test_endpoint(self):
        response = self.assert_endpoint_works("/statistics")

    def test_contents(self):
        response = self.assert_endpoint_works("/statistics")
        response = json.loads(response.data)

        assert response['status'] == 'ok'

        stats = response['statistics']

        assert all([k in stats for k in ('all', 'year', 'month', 'week', 'day')])
        for k in ('all', 'year', 'month', 'week', 'day'):
            for subk in ('top_artists', 'top_albums', 'top_users'):
                try:
                    assert subk in stats[k]
                except:
                    import ipdb; ipdb.set_trace()
