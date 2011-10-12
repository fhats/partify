import json
from urllib import quote

from testify import *

from testing.logged_in_user_test_case import LoggedInUserTestCase

class TrackTestCase(LoggedInUserTestCase):
    """Tests all of the related functions in track.py"""

    def test_track_search(self):
        response_data = self.assert_search_works_and_get_results(artist='Stars', album='Heart', title='Elevator Love Letter')
        assert response_data['status'] == 'ok'
        assert len(response_data['results']) == 1

        response_data = self.assert_search_works_and_get_results(artist='Darwin Deez')
        assert response_data['status'] == 'ok'
        assert len(response_data['results']) == 16 # 16 is the number of darwin deez songs in the sample dataset

    def test_empty_track_search(self):
        response_data = self.assert_search_works_and_get_results()
        assert response_data['status'] == 'error'
        assert 'No search criteria specified!' in response_data['message']

    def test_nonsense_track_search(self):
        response_data = self.assert_search_works_and_get_results(artist='sdafggsdad', album='sff35243', title='@$3rwesfd')
        assert response_data['status'] == 'ok'
        assert len(response_data['results']) == 0

    def test_track_search_results_in_album_order(self):
        response_data = self.assert_search_works_and_get_results(artist='Land Of Talk', album='Some Are Lakes')
        assert response_data['status'] == 'ok'
        assert len(response_data['results']) == 10

        for (track, pos) in zip(response_data['results'], range(1, 11)):
            assert int(track['track']) == pos

    def assert_search_works_and_get_results(self, artist=None, title=None, album=None):
        query_string = ""
        if artist is not None:
            query_string += "artist=%s&" % quote(artist)
        if title is not None:
            query_string += "title=%s&" % quote(title)
        if album is not None:
            query_string += "album=%s&" % quote(album)
        response = self.app.get('/track/search?%s' % query_string)
        response_data = json.loads(response.data)
        
        assert response.status_code == 200
        assert 'status' in response_data

        return response_data