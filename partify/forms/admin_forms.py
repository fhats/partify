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

from wtforms import BooleanField
from wtforms import Form 
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import TextField
from wtforms import validators

from partify.priv import priv_in_english

class ConfigurationForm(Form):
    """A WTForm for configuration information.

    Covers:
    * Last.fm information (api key, secret key)
    * MPD server information (hostname, port)
    * Server technology
    * Server host
    * Server port
    * perhaps various Mopidy settings eventually (stream bitrate, etc)
    * eventually arbitration scheme for track selection"""
    
    mpd_server_hostname = TextField("MPD Server Hostname", [validators.Required()])
    mpd_server_port = IntegerField("MPD Server Port", [validators.Required(), validators.NumberRange(min=0, max=65535)])
    server_host = TextField("Hostname to listen on", [validators.Required()])
    server_port = IntegerField("Port to listen on", [validators.Required(), validators.NumberRange(min=0, max=65535)])
    server = SelectField("Underlying Server Software", [validators.Required()], choices=[('tornado', 'Tornado'), ('builtin', 'Builtin Debugging Server')])
    lastfm_api_key = TextField("Last.fm API Key", [validators.Optional()])
    lastfm_api_secret = TextField("Last.fm API Secret", [validators.Optional()])

def create_single_user_admin_admin_form(user_id):
    """Creates a SingleUserAdminAdminForm that can be used in concert with other SingleUserAdminAdminForms."""

    class SingleUserAdminAdminForm(Form):
        pass
    
    setattr(SingleUserAdminAdminForm, "%d_admin_config" % user_id, BooleanField(priv_in_english("ADMIN_CONFIG"), [validators.Required()]))
    setattr(SingleUserAdminAdminForm, "%d_admin_playback" % user_id, BooleanField(priv_in_english("ADMIN_PLAYBACK"), [validators.Required()]))
    setattr(SingleUserAdminAdminForm, "%d_admin_admin" % user_id, BooleanField(priv_in_english("ADMIN_ADMIN"), [validators.Required()]))
    setattr(SingleUserAdminAdminForm, "%d_admin_interface" % user_id, BooleanField(priv_in_english("ADMIN_INTERFACE"), [validators.Required()]))

    return SingleUserAdminAdminForm
