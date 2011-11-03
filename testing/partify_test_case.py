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

import os
import random
import tempfile
from multiprocessing import Process

from testify import *

from partify import app
# TODO: Figure out these imports and how to remove duplication between this and run.py
from partify import ipc, on_startup, player, queue, track, user
from partify.database import init_db, db
from partify.models import User

class PartifyTestCase(TestCase):
	@class_setup
	def _prepare(self):
		self.db_fd = tempfile.mkstemp()
		app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % self.db_fd[1]
		app.config['TESTING'] = True
		ipc.init_times()
		init_db()

	@class_teardown
	def _cleanup(self):
		os.close(self.db_fd[0])
		os.unlink(self.db_fd[1])

	@setup
	def _setup(self):
		self.app = app.test_client()
	
	@teardown
	def _teardown(self):
		pass

	def create_test_user(self):
		"""Creates a test user with the same username as password."""
		r = random.Random()
		uid = r.randint(0,10000000000000)
		user = User(name='test_user_%d' % uid,
			username='%d' % uid,
			password='%d' % uid)
		db.session.add(user)
		db.session.commit()
		return user

	def assert_endpoint_works(self, endpoint):
		response = self.app.get(endpoint, follow_redirects=True)
		assert response.status_code == 200
		return response