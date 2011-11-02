from wtforms import Form 
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import TextField
from wtforms import validators

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
    
    mpd_hostname = TextField("MPD Server Hostname", [validators.Required()])
    mpd_port = IntegerField("MPD Server Port", [validators.Required(), validators.NumberRange(min=0, max=65535)])
    server_hostname = TextField("Hostname to listen on", [validators.Required()])
    server_port = IntegerField("Port to listen on", [validators.Required()])
    server_software = SelectField("Underlying Server Software", [validators.Required()], choices=[('tornado', 'Tornado'), ('builtin', 'Builtin Debugging Server')])
    lastfm_api_key = TextField("Last.fm API Key", [validators.Optional])
    lastfm_api_secret = TextField("Last.fm API Secret", [validators.Optional])
    