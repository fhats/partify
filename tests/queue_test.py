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

import json
import random
import time
from testify import *

from partify import app
from partify.models import PlayQueueEntry
from partify.queue import track_from_spotify_url
from partify.queue import track_info_from_spotify_url
from testing.data.sample_tracks import sample_tracks
from testing.mocks.mock_mpd_client import MockMPDClient
from testing.logged_in_user_test_case import LoggedInUserTestCase

class QueueTestCase(LoggedInUserTestCase):
	"""Tests all of the functions pertaining to queue management (queue.py)."""

	@setup
	def _with_mpd_client(self):
		self.mpd = MockMPDClient()

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
		assert not any([track['spotify_url'] == track_to_add['file'] for track in response_data['queue']])
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
		assert track.date == '2003'
		assert track.spotify_url == 'spotify:track:6LDYVzxjDSAO92UZ5veM3u'

	def test_track_info_from_spotify_url(self):
		track_info = track_info_from_spotify_url('spotify:track:6LDYVzxjDSAO92UZ5veM3u')
		assert track_info is not None
		assert all(k in track_info for k in ('title', 'artist', 'album', 'spotify_url', 'date', 'length'))
		assert track_info['title'] == 'Elevator Love Letter'
		assert track_info['artist'] == 'Stars'
		assert track_info['album'] == 'Heart'
		assert track_info['length'] == 243.147
		assert track_info['date'] == '2003'
		assert track_info['spotify_url'] == 'spotify:track:6LDYVzxjDSAO92UZ5veM3u'

	def random_sample_track(self):
		r = random.Random()
		return r.choice(sample_tracks)