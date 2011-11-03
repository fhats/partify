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

from partify import app
from partify import user
from partify.database import db
from partify.models import User
from testing.partify_test_case import PartifyTestCase

class UserTestCase(PartifyTestCase):
	"""Tests that test all of the logic and endpoints related to the user.

	A note to the reader: I've omitted form validation tests as I am using validators
	included as part of the WTForms project. These validators should be independently covered
	by tests from the WTForms project and as such it is not my concern to be testing them.

	In the future when I have concrete ideas about if/what user requirements need to be strictly
	validated, they *may* get tests here."""

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
		
		new_user = User.query.filter(db.and_(User.name == test_name, User.username == test_username)).first()
		assert new_user is not None
		assert new_user.name == test_name
		assert new_user.username == test_username
		assert new_user.password != test_password # The password should be stored as a hash!

	def test_user_login(self):
		user = self.create_test_user()

		# We know that create_test_user always makes a test user with the password the same
		# as the username.
		response = self.app.post('/login',
			data = {'username': user.username, 'password': user.username},
			follow_redirects = True)
		assert response.status_code == 200
		assert """<form method="POST" action="/login">""" not in response.data
		assert "Account settings" in response.data

	def test_no_user_login(self):
		response = self.app.get('/', follow_redirects = True)
		assert response.status_code == 200
		assert """<form method="POST" action="/login">""" in response.data
		assert "Account settings" not in response.data

		response = self.app.get('/player', follow_redirects = True)
		assert response.status_code == 200
		assert """<form method="POST" action="/login">""" in response.data
		assert "Account settings" not in response.data

	def test_invalid_user_login(self):
		response = self.app.post('/login',
			data = {'username': 'test_user', 'password':'test_user'},
			follow_redirects = True)
		assert response.status_code == 200
		assert """<form method="POST" action="/login">""" in response.data
		assert "Account settings" not in response.data

	def test_user_logout(self):
		user = self.create_test_user()

		# We know that create_test_user always makes a test user with the password the same
		# as the username.
		response = self.app.post('/login',
			data = {'username': user.username, 'password': user.username},
			follow_redirects = True)
		assert response.status_code == 200
		assert """<form method="POST" action="/login">""" not in response.data
		assert "Account settings" in response.data

		response = self.app.get('/logout', follow_redirects=True)
		assert """<form method="POST" action="/login">""" in response.data
		assert "Account settings" not in response.data

		# make sure session stuff doesn't stick around
		response = self.app.get('/', follow_redirects = True)
		assert response.status_code == 200
		assert """<form method="POST" action="/login">""" in response.data
		assert "Account settings" not in response.data
		