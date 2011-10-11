from testify import *

from testing.partify_test_case import PartifyTestCase

class PlayerTestCase(PartifyTestCase):
	"""A test case for the player (player.py) functions, mostly the endpoints just to make sure they work."""

	def test_player_endpoint(self):
		raise NotImplementedError

	def test_player_status(self):
		raise NotImplementedError

	def test_get_global_queue(self):
		raise NotImplementedError

	def test_get_user_queue(self):
		raise NotImplementedError