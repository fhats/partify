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
		