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

from partify.database import db
from partify.models import User

privs = {
    "ADMIN_CONFIG": 0x01,
    "ADMIN_PLAYBACK": 0x02,
    "ADMIN_ADMIN": 0x04,
    "ADMIN_INTERFACE": 0x08
}

privs_in_english = {
    "ADMIN_CONFIG": "Modify configuration settings",
    "ADMIN_PLAYBACK": "Access playback controls",
    "ADMIN_ADMIN": "Modify user privileges",
    "ADMIN_INTERFACE": "View administration interface"
}

def give_user_privilege(user, priv):
    """Given a user (either a User type or an ID) set the given privilege (identified by string) in the user's privilege list."""
    if not isinstance(user, User):
        user = User.query.get(user)
    # Set the appropriate bit in the user's privileges bitfield
    user.privs |= privs[priv]
    db.session.commit()

def revoke_user_privilege(user, priv):
    """Given a user (either a User type or an ID) remove the given privilege (identified by string) in the user's privilege list."""
    if not isinstance(user, User):
        user = User.query.get(user)
    user.privs &= (~privs[priv])
    db.session.commit()

def user_has_privilege(user, priv):
    if not isinstance(user, User):
        user = User.query.get(user)
    return user.privs & privs[priv] > 0

def dump_user_privileges(user):
    if not isinstance(user, User):
        user = User.query.get(user)
    return [p for p, v in privs.iteritems() if user.privs & v != 0]

def priv_in_english(priv):
    return privs_in_english[priv]