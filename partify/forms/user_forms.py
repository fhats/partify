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

from wtforms import Form 
from wtforms import PasswordField
from wtforms import TextField
from wtforms import validators

class SettingsForm(Form):
    name = TextField("Display Name", [validators.Required(), validators.Length(min=4, max=64)])
    current_password = PasswordField("Current Password")
    new_password = PasswordField("New Password", [validators.EqualTo('confirm_password', message="Passwords must match!")])
    confirm_password = PasswordField("Confirm Password")

class RegistrationForm(Form):
    name = TextField("Your Name", [validators.Required(), validators.Length(min=4, max=64)])
    username = TextField('Username', [validators.Length(min=4, max=36), validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=1)])

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=36), validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=1)])
