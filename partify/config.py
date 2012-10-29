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

"""A collection of functions to simplify storing and retrieving configuration
in YAML files."""
import copy
import hashlib
import random
import time
import yaml

from partify import app


def _produce_random_data():
    """Produces a SHA512 hash of the concatenation of 5000 random numbers (as a string).
    Used by ``default_configuration`` to set the ``SECRET_KEY`` and ``SESSION_SALT``
    configuration fields.

    :returns: A string of random data
    :rtype: string
    """
    m = hashlib.sha512()
    m.update(str(time.time()))
    for i in range(1, 5000):
        m.update(str(random.random()))
    return m.hexdigest()


# Default configuration values in case they aren't set at load time
default_configuration = {
    'DEBUG': True,
    'LASTFM_API_KEY': '',
    'LASTFM_API_SECRET': '',
    'MPD_SERVER_HOSTNAME': 'localhost',
    'MPD_SERVER_PORT': 6600,
    'PROFILE': False,
    'SECRET_KEY': _produce_random_data(),
    'SELECTION_SCHEME': 'ROUND_ROBIN',
    'SERVER': 'tornado',
    'SERVER_HOST': '0.0.0.0',
    'SERVER_PORT': 5000,
    'SESSION_SALT': _produce_random_data(),
    'TESTING': False
}

# Transformations to be performed on the key in case the user specifies the wrong type
transformations = {
    'DEBUG': lambda x: bool(int(x)),
    'MPD_SERVER_PORT': int,
    'PROFILE': lambda x: bool(int(x)),
    'SERVER_PORT': int,
    'TESTING': lambda x: bool(int(x))
}


def load_config_from_yaml(config_path=None):
    """Loads configuration information from the YAML file specified by
    ``config_path``.

    If config_path can't be loaded, we load a default configuration (specified
    ``default_configuration``) instead. Each configuration value is also
    run through the transformer with the corresponding key in
    ``transformations``. Configuration is stored in ``app.config``. If
    ``config_path`` is not specified, ``partify.yaml`` is tried.

    :param config_path: The path to try to load configuration from. [partify.yaml]
    :type config_path: string
    """

    if not config_path:
        config_path = "partify.yaml"

    app.config['config_path'] = config_path

    try:
        with open(config_path) as config_file:
            config = yaml.load(config_file.read()) or {}
    except IOError:
        # The configuration file specified couldn't be read
        # Let's just load a default configuration and send up a warning
        app.logger.warning("Failed to load configuration file %s. Using defaults instead." % config_path)
        config = copy.deepcopy(default_configuration)

    for key in set(config.keys() + default_configuration.keys()):
        transform = transformations.get(key, lambda x: x)
        value = config.get(key, default_configuration[key])
        app.config[key] = transform(value)


def set_config_value(field, value):
    """Sets the configuration value specified in ``field`` to the value given in
    ``value``.

    :param field: The configuration field to change
    :type field: string
    :param value: The new value of ``field``
    :type value: yaml serializable type
    """
    old_value = app.config.get(field, None)
    app.config[field] = value

    if value != old_value:
        with open(app.config['config_path'], 'w') as config_file:
            config_file.write(yaml.dump(app.config))
