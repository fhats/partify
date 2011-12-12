# Copyright 2011 Fred Hatfull
#
# This file is part of Partify.
#
# Partify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Partify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Partify.  If not, see <http://www.gnu.org/licenses/>.

import json

from testify import *

from partify import app
from partify import admin
from partify.admin import create_admin_admin_form
from partify.config import get_config_value
from partify.database import db
from partify.forms.admin_forms import ConfigurationForm
from partify.models import User
from partify.priv import dump_user_privileges, give_user_privilege, revoke_user_privilege, user_has_privilege
from testing.logged_in_user_test_case import LoggedInUserTestCase
from testing.mocks.mock_mpd_client import MockMPDClient

class AdminTestCase(LoggedInUserTestCase):
    """Tests that cover the logic for the administrative functions."""

    @setup
    def setup(self):
        # Make sure the user that is testing has administrative privileges
        give_user_privilege(self.user, "ADMIN_INTERFACE")
        self.mpd = MockMPDClient()

    def test_admin_console(self):
        response = self.assert_endpoint_works('/admin')
        assert "<h2>Administration</h2>" in response.data
        assert "<h4>Configuration</h4>" not in response.data
        assert "<h4>Player Controls</h4>" not in response.data
        assert "<h4>User Administration</h4>" not in response.data

        # Ensure that the proper segments get shown with the corresponding privileges
        give_user_privilege(self.user, "ADMIN_CONFIG")
        response = self.assert_endpoint_works('/admin')
        assert "<h2>Administration</h2>" in response.data
        assert "<h4>Configuration</h4>" in response.data
        assert "<h4>Player Controls</h4>" not in response.data
        assert "<h4>User Administration</h4>" not in response.data

        give_user_privilege(self.user, "ADMIN_PLAYBACK")
        response = self.assert_endpoint_works('/admin')
        assert "<h2>Administration</h2>" in response.data
        assert "<h4>Configuration</h4>" in response.data
        assert "<h4>Player Controls</h4>" in response.data
        assert "<h4>User Administration</h4>" not in response.data

        give_user_privilege(self.user, "ADMIN_ADMIN")
        response = self.assert_endpoint_works('/admin')
        assert "<h2>Administration</h2>" in response.data
        assert "<h4>Configuration</h4>" in response.data
        assert "<h4>Player Controls</h4>" in response.data
        assert "<h4>User Administration</h4>" in response.data

    def test_configuration_update(self):
        give_user_privilege(self.user, "ADMIN_CONFIG")

        form_object = dict( ( (k.lower(),v) for k,v in app.config.iteritems()) )
        configuration_form = ConfigurationForm(**form_object)

        configuration_form.server_port.data = 10000

        response = self.app.post("/admin/config_update", 
            data=configuration_form.data,
            follow_redirects = True)

        assert response.status_code == 200
        assert int(get_config_value("SERVER_PORT")) == 10000

    def test_admin_admin_update(self):
        give_user_privilege(self.user, "ADMIN_ADMIN")

        user_id = self.user.id

        forms = create_admin_admin_form()

        my_form = forms[user_id]
        my_form["%d_admin_config" % user_id].data = True
        my_form["%d_admin_admin" % user_id].data = True
        my_form["%d_admin_playback" % user_id].data = True
        my_form["%d_admin_interface" % user_id].data = True

        forms[user_id] = my_form

        # Create a big dict to send back, just like in the real world!
        post_data = {}
        for form in forms.itervalues():
            post_data.update(form.data)

        # Try to update our own privileges!
        response = self.app.post("/admin/admin_admin_update",
            data=post_data,
            follow_redirects=True)

        assert response.status_code == 200
        assert user_has_privilege(user_id, "ADMIN_INTERFACE")
        assert user_has_privilege(user_id, "ADMIN_CONFIG")
        assert user_has_privilege(user_id, "ADMIN_PLAYBACK")
        assert user_has_privilege(user_id, "ADMIN_ADMIN")

    def test_admin_play(self):
        give_user_privilege(self.user, "ADMIN_PLAYBACK")

        self.assert_endpoint_works("/admin/playback/play")

    def test_admin_pause(self):
        give_user_privilege(self.user, "ADMIN_PLAYBACK")

        self.assert_endpoint_works("/admin/playback/pause")

    def test_admin_skip(self):
        give_user_privilege(self.user, "ADMIN_PLAYBACK")

        self.assert_endpoint_works("/admin/playback/skip")

    def test_admin_clear(self):
        give_user_privilege(self.user, "ADMIN_PLAYBACK")

        self.assert_endpoint_works("/admin/queue/clear")
