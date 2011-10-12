import json
import random
import time
from testify import *

from testing.data.sample_tracks import sample_tracks
from testing.mocks.mock_mpd_client import MockMPDClient
from testing.logged_in_user_test_case import LoggedInUserTestCase

class PlayerTestCase(LoggedInUserTestCase):
    """A test case for the player (player.py) functions, mostly the endpoints just to make sure they work."""

    @setup
    def _queue_tracks(self):
        r = random.Random()
        sample_tracks_copy = sample_tracks
        r.shuffle(sample_tracks_copy)

        for track in sample_tracks_copy[:5]:
            response = self.app.post('/queue/add', data = {'spotify_uri': track['file']})
            
            response_data = json.loads(response.data)
            assert response.status_code == 200
            assert response_data['status'] == 'ok'
        
        self.added_tracks = sample_tracks_copy[:5]

        self.mpd = MockMPDClient()

    def test_player_endpoint(self):
        response = self.assert_endpoint_works('/player')
        assert 'Account settings' in response.data

    def test_player_status(self):
        response = self.assert_endpoint_works('/player/status/poll')
        response_data = json.loads(response.data)
        assert response.status_code == 200

        for track in self.added_tracks:
            assert track['file'] in [t['spotify_url'] for t in response_data['user_queue']]
            assert track['file'] in [t['spotify_url'] for t in response_data['global_queue']]
        
        pl_update = int(response_data['last_global_playlist_update'])

        response = self.app.get('/player/status/poll?current=%s' % pl_update)
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert 'user_queue' not in response_data
        assert 'global_queue' not in response_data

        # This is needed for now to emulate how the client stores times :(
        time.sleep(2)

        self.mpd.addid('spotify:track:6LDYVzxjDSAO92UZ5veM3u')

        response = self.app.get('/player/status/poll?current=%s' % pl_update)
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert 'user_queue' in response_data
        assert 'global_queue' in response_data