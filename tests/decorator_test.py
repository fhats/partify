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
from flask import jsonify
from testify import *

from partify import app
from partify.decorators import with_authentication, with_mpd
from testing.partify_test_case import PartifyTestCase

class DecoratorTestCase(PartifyTestCase):
	"""A quick and dirty test of the decorators used in Partify."""

	def test_with_authentication(self):
		"""Adds a new route to the app on-the-fly to test the authentication decorator."""
		@app.route('/test_auth')
		@with_authentication
		def _tested_wrapped_fn():
			return jsonify(status='ok')
		
		response = self.app.get('/test_auth', follow_redirects=True)
		assert response.status_code == 200
		assert """<form method="POST" action="/login">""" in response.data
		assert "Account settings" not in response.data
		
		# Now test logging in
		user = self.create_test_user()

		response = self.app.post('/login',
			data = {'username': user.username, 'password': user.username},
			follow_redirects = True)
		assert response.status_code == 200
		response = self.app.get('/test_auth', follow_redirects=True)
		assert response.status_code == 200
		response_data = json.loads(response.data)
		assert 'status' in response_data
		assert response_data['status'] == 'ok'

	def test_with_mpd(self):
		@with_mpd
		def _tested_wrapped_fn(mpd):
			return mpd is not None

		assert _tested_wrapped_fn() is True
