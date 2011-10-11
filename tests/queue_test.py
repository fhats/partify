from testify import *

from testing.partify_test_case import PartifyTestCase

class QueueTestCase(PartifyTestCase):
	"""Tests all of the functions pertaining to queue management (queue.py)."""

	def test_queue_add(self):
		raise NotImplementedError

	def test_queue_add_bad_track(self):
		raise NotImplementedError

	def test_queue_remove(self):
		raise NotImplementedError

	def test_queue_remove_bad_track(self):
		raise NotImplementedError

	def test_queue_remove_nonexistent_track(self):
		raise NotImplementedError

	def test_queue_remove_unowned_track(self):
		raise NotImplementedError

	def test_queue_reorder_tracks(self):
		raise NotImplementedError

	def test_user_queue_list(self):
		raise NotImplementedError

	def test_track_from_spotify_url(self):
		raise NotImplementedError

	def test_track_info_from_spotify_url(self):
		raise NotImplementedError

	def test_playlist_consistency_mechanism(self):
		raise NotImplementedError

	def test_playlist_updated_watcher(self):
		raise NotImplementedError