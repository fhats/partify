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
from partify.config import _produce_random_data, load_config_from_yaml, set_config_value
from testing.partify_test_case import PartifyTestCase


class ConfigTestCase(PartifyTestCase):
    """Test coverage for configuration-related functions."""

    def test_loaded_types(self):
        load_config_from_yaml(self.config_path)

        assert isinstance(app.config["DEBUG"], bool)
        assert isinstance(app.config["MPD_SERVER_PORT"], int)
        assert isinstance(app.config["PROFILE"], bool)
        assert isinstance(app.config["SERVER_PORT"], int)
        assert isinstance(app.config["TESTING"], bool)
        set_config_value("TESTING", True)

    def test_sensible_defaults(self):
        # Remove any existing configuration values for the stuff we get defaults for

        for key in ("DEBUG", "LASTFM_API_KEY", "LASTFM_API_SECRET", "MPD_SERVER_HOSTNAME",
            "MPD_SERVER_PORT", "PROFILE", "SERVER"):
            del app.config[key]

        load_config_from_yaml(self.config_path)

        assert app.config["DEBUG"] == True
        assert app.config["LASTFM_API_KEY"] == ""
        assert app.config["LASTFM_API_SECRET"] == ""
        assert app.config["MPD_SERVER_HOSTNAME"] == "localhost"
        assert app.config["MPD_SERVER_PORT"] == 6600
        assert app.config["PROFILE"] == False
        assert app.config["SERVER"] == "tornado"

        set_config_value("TESTING", True)

    def test_set_get_config_value(self):
        set_config_value("DUMMY", "Initial")
        assert app.config["DUMMY"] == "Initial"
        set_config_value["DUMMY", "Updated"]
        assert get_config_value("DUMMY") == "Updated"

    def test_produce_random_data(self):
        # Just make sure the fn doesnt crash
        _produce_random_data()
