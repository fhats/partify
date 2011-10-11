from sqlalchemy import and_
from testify import *

from partify import app
from partify import user
from partify.models import User
from testing.partify_test_case import PartifyTestCase

class UserTestCase(PartifyTestCase):

	@setup
	def setup(self):
		# TODO: Make sure the session is clear before doing any of these tests
		pass
	
	@teardown
	def cleanup(self):
		# TODO: Make sure the session is clear after doing any of these tests
		pass

	"""A few tests to make sure the endpoints work OK."""
	def test_registration_form(self):
		self.assert_endpoint_works('/register')

	def test_login_form(self):
		self.assert_endpoint_works('/login')

	def test_logout_endpoint(self):
		self.assert_endpoint_works('/logout')

	"""Tests related to views that actually have logic."""
	def test_user_registration(self):
		"""Test that user registration works."""
		test_name = 'tester'
		test_username = 'test_user'
		test_password = 'test_password'
		response = self.app.post('/register',
			data = {'name': test_name, 'username': test_username, 'password': test_password},
			follow_redirects = True
		)
		assert response.status_code == 200
		
		new_user = User.query.filter(and_(User.name == test_name, User.username == test_username)).first()
		assert new_user is not None
		assert new_user.name == test_name
		assert new_user.username == test_username
		assert new_user.password != test_password # The password should be stored as a hash!

	def test_user_registration_name_too_long(self):
		raise NotImplementedError

	def test_user_registration_username_too_long(self):
		raise NotImplementedError
	
	def test_user_registration_name_missing(self):
		raise NotImplementedError

	def test_user_registration_username_missing(self):
		raise NotImplementedError

	def test_user_login(self):
		user = self.create_test_user()


	"""Utility functions."""
	def assert_endpoint_works(self, endpoint):
		response = self.app.get(endpoint, follow_redirects=True)
		assert response.status_code == 200