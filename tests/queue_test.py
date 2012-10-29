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
import time
from itertools import cycle, dropwhile

from testify import *

from partify import app
from partify.config import get_config_value, load_config_from_db, set_config_value
from partify.database import db
from partify.models import PlayQueueEntry, Vote
from partify.queue import add_track_from_spotify_url
from partify.queue import _ensure_mpd_playlist_consistency
from partify.queue import track_from_mpd_search_results
from partify.queue import track_from_spotify_url
from partify.queue import track_info_from_mpd_search_results
from partify.queue import track_info_from_spotify_url
from testing.data.sample_tracks import sample_tracks
from testing.mocks.mock_mpd_client import MockMPDClient
from testing.logged_in_user_test_case import LoggedInUserTestCase

class QueueTestCase(LoggedInUserTestCase):
    """Tests all of the functions pertaining to queue management (queue.py)."""

    @setup
    def _with_mpd_client(self):
        self.mpd = MockMPDClient()

    @teardown
    def _without_mpd_client(self):
        self.mpd.stop_idle()

    def test_queue_add(self):
        track_to_add = self.random_sample_track()

        response = self.app.post('/queue/add', data = {'spotify_uri': track_to_add['file']})

        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['status'] == 'ok'
        assert response_data['file'] == track_to_add['file']
        assert any([track['spotify_url'] == track_to_add['file'] for track in response_data['queue']])
        assert track_to_add in self.mpd.playlistinfo()

    def test_queue_add_bad_track(self):
        track_to_add = 'ERk;lw343##'
        response = self.app.post('/queue/add', data = {'spotify_uri': track_to_add})

        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['status'] != 'ok'
        assert response_data['status'] == 'error'
        assert 'invalid' in response_data['message']

    def test_queue_add_no_track(self):
        response = self.app.post('/queue/add', data = {})
        assert response.status_code != 200

    def test_queue_remove(self):
        track_to_add = self.random_sample_track()

        response = self.app.post('/queue/add', data = {'spotify_uri': track_to_add['file']})

        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['status'] == 'ok'

        added_track = [track for track in response_data['queue'] if track['spotify_url'] == track_to_add['file']][0]
        added_mpd_id = added_track['mpd_id']

        response = self.app.post('/queue/remove', data = {'track_id': added_mpd_id})
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert response_data['status'] == 'ok'
        assert track_to_add not in self.mpd.playlistinfo()

    def test_queue_remove_bad_track(self):
        track_to_add = self.random_sample_track()

        response = self.app.post('/queue/add', data = {'spotify_uri': track_to_add['file']})

        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['status'] == 'ok'

        added_track = [track for track in response_data['queue'] if track['spotify_url'] == track_to_add['file']][0]
        added_mpd_id = added_track['mpd_id']

        response = self.app.post('/queue/remove', data = {'track_id': 'kjffdgfsfsasfdghhjkghf'})
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert response_data['status'] != 'ok'
        assert response_data['status'] == 'error'
        assert 'Not a valid track ID!' in response_data['message']
        assert track_to_add in self.mpd.playlistinfo()

    def test_queue_remove_nonexistent_track(self):
        track_to_add = self.random_sample_track()

        response = self.app.post('/queue/add', data = {'spotify_uri': track_to_add['file']})

        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['status'] == 'ok'

        added_track = [track for track in response_data['queue'] if track['spotify_url'] == track_to_add['file']][0]
        added_mpd_id = added_track['mpd_id']

        response = self.app.post('/queue/remove', data = {'track_id': '4354565745353534'})
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert response_data['status'] != 'ok'
        assert response_data['status'] == 'error'
        assert 'Could not find track with id' in response_data['message']
        assert track_to_add in self.mpd.playlistinfo()

    def test_queue_remove_unowned_track(self):
        other_user = self.create_test_user()
        other_user_client = app.test_client()
        # Log the 'other' user in
        other_user_client.post('/login', data = {'username': other_user.username, 'password': other_user.username}, follow_redirects = True)

        track_to_add = self.random_sample_track()

        response = other_user_client.post('/queue/add', data = {'spotify_uri': track_to_add['file']})
        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['status'] == 'ok'

        added_track = [track for track in response_data['queue'] if track['spotify_url'] == track_to_add['file']][0]
        added_mpd_id = added_track['mpd_id']

        response = self.app.post('/queue/remove', data = {'track_id': added_mpd_id})
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert response_data['status'] != 'ok'
        assert response_data['status'] == 'error'
        assert 'You are not authorized' in response_data['message']
        assert track_to_add in self.mpd.playlistinfo()

    def test_queue_reorder_tracks(self):
        # Add a bunch of tracks.
        tracks_to_add = [track for track in sample_tracks if track['album'] == 'Some Are Lakes']

        for track_to_add in tracks_to_add:
            response = self.app.post('/queue/add', data = {'spotify_uri': track_to_add['file']})

            response_data = json.loads(response.data)
            assert response.status_code == 200
            assert response_data['status'] == 'ok'

        r = random.Random()
        pqe_ids = [track['id'] for track in response_data['queue']]
        priorities = range(1, len(pqe_ids) + 1)
        r.shuffle(pqe_ids)
        r.shuffle(priorities)
        new_priorities = dict( (pqe_id, priority) for (pqe_id, priority) in zip(pqe_ids, priorities) )

        response = self.app.post('/queue/reorder', data = new_priorities)
        response_data = json.loads(response.data)
        assert response.status_code == 200
        assert response_data['status'] == 'ok'

    def test_user_queue_list(self):
        r = random.Random()
        # Add a bunch of tracks.
        tracks_to_add = [track for track in sample_tracks if track['album'] == 'Set Yourself On Fire']
        r.shuffle(tracks_to_add)

        for track_to_add in tracks_to_add:
            response = self.app.post('/queue/add', data = {'spotify_uri': track_to_add['file']})

            response_data = json.loads(response.data)
            assert response.status_code == 200
            assert response_data['status'] == 'ok'

        response = self.assert_endpoint_works('/queue/list')
        response_data = json.loads(response.data)

        assert response_data['status'] == 'ok'
        for track in tracks_to_add:
            assert any([response_track['spotify_url'] == track['file'] for response_track in response_data['result']])

    def test_track_from_spotify_url(self):
        track = track_from_spotify_url('spotify:track:6LDYVzxjDSAO92UZ5veM3u')
        assert track is not None
        assert track.title == 'Elevator Love Letter'
        assert track.artist == 'Stars'
        assert track.album == 'Heart'
        assert track.length == 243.147
        assert track.date == '2003' or track.date == '2003-01-01'
        assert track.spotify_url == 'spotify:track:6LDYVzxjDSAO92UZ5veM3u'

    def test_track_info_from_spotify_url(self):
        track_info = track_info_from_spotify_url('spotify:track:6LDYVzxjDSAO92UZ5veM3u')
        assert track_info is not None
        assert all(k in track_info for k in ('title', 'artist', 'album', 'spotify_url', 'date', 'length'))
        assert track_info['title'] == 'Elevator Love Letter'
        assert track_info['artist'] == 'Stars'
        assert track_info['album'] == 'Heart'
        assert track_info['length'] == 243.147
        assert track_info['date'] == '2003' or track.date == '2003-01-01'
        assert track_info['spotify_url'] == 'spotify:track:6LDYVzxjDSAO92UZ5veM3u'

    def test_track_from_mpd_search_results(self):
        track = track_from_mpd_search_results('spotify:track:6LDYVzxjDSAO92UZ5veM3u', self.mpd)
        assert track is not None
        assert track.title == 'Elevator Love Letter'
        assert track.artist == 'Stars'
        assert track.album == 'Heart'
        assert track.length == 243.147
        assert track.date == '2003-01-01' or track.date == '2003'
        assert track.spotify_url == 'spotify:track:6LDYVzxjDSAO92UZ5veM3u'

    def test_track_info_from_mpd_search_results(self):
        track_info = track_info_from_spotify_url('spotify:track:6LDYVzxjDSAO92UZ5veM3u')
        assert track_info is not None
        assert all(k in track_info for k in ('title', 'artist', 'album', 'spotify_url', 'date', 'length'))
        assert track_info['title'] == 'Elevator Love Letter'
        assert track_info['artist'] == 'Stars'
        assert track_info['album'] == 'Heart'
        assert track_info['length'] == 243.147
        assert track_info['date'] == '2003' or track.date == '2003-01-01'
        assert track_info['spotify_url'] == 'spotify:track:6LDYVzxjDSAO92UZ5veM3u'

    def test_nxtrack_purge(self):
        self.mpd.clear()
        track = track_from_spotify_url("spotify:track:6LDYVzxjDSAO92UZ5veM3u")
        self.db.session.add(PlayQueueEntry(track=track, mpd_id=0))
        self.db.session.commit()
        _ensure_mpd_playlist_consistency(self.mpd)
        assert len(self.mpd.playlistinfo()) == 0
        assert len(PlayQueueEntry.query.all()) == 0

    def test_add_anon_track(self):
        self.mpd.clear()
        _ensure_mpd_playlist_consistency(self.mpd)
        self.mpd.addid("spotify:track:6LDYVzxjDSAO92UZ5veM3u")
        _ensure_mpd_playlist_consistency(self.mpd)
        assert len(self.mpd.playlistinfo()) == 1
        assert len(PlayQueueEntry.query.all()) == 1
        db_entry = PlayQueueEntry.query.first()
        assert db_entry.track.spotify_url == "spotify:track:6LDYVzxjDSAO92UZ5veM3u"
        assert db_entry.user is None

    @suite('transient')
    def test_round_robin_selection(self):
        set_config_value('SELECTION_SCHEME', 'ROUND_ROBIN')
        load_config_from_db()
        self.mpd.clear()
        _ensure_mpd_playlist_consistency(self.mpd)
        assert len(self.mpd.playlistinfo()) == 0
        assert len(PlayQueueEntry.query.all()) == 0

        # Simulate 5 users queueing up 10 tracks each in serial
        users = []
        for i in range(1, 4):
            user = self.create_test_user()
            users.append(user)
            for ii in range(1, 4):
                track = self.random_sample_track()
                add_track_from_spotify_url(self.mpd, track['file'], user.id)

        first_user = users[0]
        users = sorted(users, key=lambda x: x.username)
        users = cycle(users)
        users = dropwhile(lambda x: x != first_user, users)

        # Simulate the callback chain that would occur in the wild
        last_order = []
        while last_order != [i['id'] for i in self.mpd.playlistinfo()]:
            last_order = [i['id'] for i in self.mpd.playlistinfo()]
            _ensure_mpd_playlist_consistency(self.mpd)

        mpd_playlist = self.mpd.playlistinfo()
        db_tracks = PlayQueueEntry.query.order_by(PlayQueueEntry.playback_priority.asc()).all()

        for (pqe, mpd_track) in zip(db_tracks, mpd_playlist):
            assert pqe.playback_priority == mpd_track['pos']

        for (pqe, prop_user) in zip(db_tracks, users):
            assert pqe.user == prop_user

    @suite('transient')
    def test_fcfs_selection(self):
        set_config_value('SELECTION_SCHEME', 'FCFS')
        load_config_from_db()
        self.mpd.clear()
        _ensure_mpd_playlist_consistency(self.mpd)
        assert len(self.mpd.playlistinfo()) == 0
        assert len(PlayQueueEntry.query.all()) == 0

        # Simulate 5 users queueing up 10 tracks each in serial
        users = []
        for i in range(1, 4):
            user = self.create_test_user()
            for i in range(1, 4):
                users.append(user)
                track = self.random_sample_track()
                add_track_from_spotify_url(self.mpd, track['file'], user.id)

        # Simulate the callback chain that would occur in the wild
        last_order = []
        while last_order != [i['id'] for i in self.mpd.playlistinfo()]:
            last_order = [i['id'] for i in self.mpd.playlistinfo()]
            _ensure_mpd_playlist_consistency(self.mpd)

        mpd_playlist = self.mpd.playlistinfo()
        db_tracks = PlayQueueEntry.query.order_by(PlayQueueEntry.playback_priority.asc()).all()

        for (pqe, mpd_track) in zip(db_tracks, mpd_playlist):
            assert pqe.playback_priority == mpd_track['pos']

        for (pqe, prop_user) in zip(db_tracks, users):
            assert pqe.user == prop_user

    @suite('transient')
    def test_fcfs_with_voting_selection(self):
        set_config_value('SELECTION_SCHEME', 'FCFS_VOTE')
        load_config_from_db()
        self.mpd.clear()
        _ensure_mpd_playlist_consistency(self.mpd)
        assert len(self.mpd.playlistinfo()) == 0
        assert len(PlayQueueEntry.query.all()) == 0

        user1 = self.create_test_user()
        user2 = self.create_test_user()

        tracks = []

        for i in range(1,11):
            st = self.random_sample_track()
            tracks.append(add_track_from_spotify_url(self.mpd, st['file'], user1.id))

        # Simulate the callback chain that would occur in the wild
        last_order = []
        while last_order != [i['id'] for i in self.mpd.playlistinfo()]:
            last_order = [i['id'] for i in self.mpd.playlistinfo()]
            _ensure_mpd_playlist_consistency(self.mpd)

        for mpd_track, expected_track in zip(self.mpd.playlistinfo(), tracks):
            assert mpd_track['file'] == expected_track.spotify_url

        r = random.Random()
        pqes = PlayQueueEntry.query.order_by(PlayQueueEntry.time_added).all()
        up_voted = []
        down_voted = []
        for i in range(1,4):
            pqe = r.choice(pqes)
            pqes.remove(pqe)
            up_voted.append(pqe)
            vote = Vote(user=user2, pqe=pqe, direction=1)
            db.session.add(vote)

        for i in range(1,4):
            pqe = r.choice(pqes)
            pqes.remove(pqe)
            down_voted.append(pqe)
            vote = Vote(user=user2, pqe=pqe, direction=-1)
            db.session.add(vote)

        db.session.commit()

        up_voted = sorted(up_voted, key=lambda x: x.time_added)
        down_voted = sorted(down_voted, key=lambda x: x.time_added)
        expected_order = up_voted + pqes + down_voted

        # Simulate the callback chain that would occur in the wild
        last_order = []
        while last_order != [i['id'] for i in self.mpd.playlistinfo()]:
            last_order = [i['id'] for i in self.mpd.playlistinfo()]
            _ensure_mpd_playlist_consistency(self.mpd)

        for mpd_track, expected_track in zip(self.mpd.playlistinfo(), expected_order):
            assert mpd_track['file'] == expected_track.track.spotify_url


    def random_sample_track(self):
        r = random.Random()
        return r.choice(sample_tracks)
