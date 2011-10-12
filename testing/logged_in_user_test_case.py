from testify import *

from testing.partify_test_case import PartifyTestCase

class LoggedInUserTestCase(PartifyTestCase):
	"""A base test case for features that just need a logged in user."""

	@setup
	def _setup_logged_in_user(self):
		self.user = self.create_test_user()
		self.app.post('/login',
			data = {'username': self.user.username, 'password': self.user.username},
			follow_redirects = True)
		