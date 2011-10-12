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
