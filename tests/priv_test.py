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

from testify import *

from partify import app
from partify.database import db
from partify.priv import dump_user_privileges, privs, give_user_privilege, revoke_user_privilege, user_has_privilege
from testing.partify_test_case import PartifyTestCase

class PrivTestCase(PartifyTestCase):

    @setup
    def setup(self):
        self.user = self.create_test_user()
        for p in privs.iterkeys():
            revoke_user_privilege(self.user, p)

    def test_give_user_privilege(self):
        give_user_privilege(self.user, "ADMIN_INTERFACE")

        assert self.user.privs & privs["ADMIN_INTERFACE"] > 0

        give_user_privilege(self.user, "ADMIN_PLAYBACK")

        assert self.user.privs & privs["ADMIN_PLAYBACK"] > 0

        give_user_privilege(self.user, "ADMIN_ADMIN")

        assert self.user.privs & privs["ADMIN_ADMIN"] > 0

        give_user_privilege(self.user, "ADMIN_CONFIG")

        assert self.user.privs & privs["ADMIN_CONFIG"] > 0

    def test_revoke_user_privilege(self):
        self.user.privs = 0xff
        db.session.add(self.user)
        db.session.commit()

        revoke_user_privilege(self.user, "ADMIN_INTERFACE")
        assert self.user.privs & privs["ADMIN_INTERFACE"] == 0
        revoke_user_privilege(self.user, "ADMIN_PLAYBACK")
        assert self.user.privs & privs["ADMIN_PLAYBACK"] == 0
        revoke_user_privilege(self.user, "ADMIN_ADMIN")
        assert self.user.privs & privs["ADMIN_ADMIN"] == 0
        revoke_user_privilege(self.user, "ADMIN_CONFIG")
        assert self.user.privs & privs["ADMIN_CONFIG"] == 0

    def test_dump_user_privileges(self):
        assert dump_user_privileges(self.user) == []

        give_user_privilege(self.user, "ADMIN_INTERFACE")
        assert "ADMIN_INTERFACE" in dump_user_privileges(self.user)

    def test_user_has_privilege(self):
        assert not user_has_privilege(self.user, "ADMIN_INTERFACE")

        give_user_privilege(self.user, "ADMIN_INTERFACE")
        assert user_has_privilege(self.user, "ADMIN_INTERFACE")
