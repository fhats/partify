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

"""Contains forms needed for user interactions, such as registering a new user or logging in."""

from wtforms import Form 
from wtforms import PasswordField
from wtforms import TextField
from wtforms import validators

class SettingsForm(Form):
    """A form for soliciting a change in settings for the user."""
    name = TextField("Display Name", [validators.Required(), validators.Length(min=1, max=32)])
    current_password = PasswordField("Current Password")
    new_password = PasswordField("New Password", [validators.EqualTo('confirm_password', message="Passwords must match!")])
    confirm_password = PasswordField("Confirm Password")

class RegistrationForm(Form):
    """A form for handling registration information."""
    name = TextField("Your Name", [validators.Required(), validators.Length(min=1, max=32)])
    username = TextField('Username', [validators.Length(min=1, max=32), validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=1)])

class LoginForm(Form):
    """A form for taking login data."""
    username = TextField('Username', [validators.Length(min=1, max=32), validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=1)])
