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

"""A collection of functions to simplify storing and retrieving configuration values
in the database."""

import hashlib
import random
import time
from tempfile import mkstemp

from partify import app
from partify.database import db
from partify.models import ConfigurationField

def load_config_from_db():
    """Loads configuration fields from the database and throws them in the Partify config dict.
    This should be used to reload configuration values after they have changed. If a configuration
    field is not in the database that field is automatically populated from a list of defaults."""
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

    # Transformations to be performed on the key in the DB in case it shouldn't be just a string
    transformations = {
        'DEBUG': lambda x: bool(int(x)),
        'MPD_SERVER_PORT': int,
        'PROFILE': lambda x: bool(int(x)),
        'SERVER_PORT': int,
        'TESTING': lambda x: bool(int(x))
    }

    all_config_fields = ConfigurationField.query.all()

    for cfg_field in all_config_fields:
        field = cfg_field.field_name
        value = cfg_field.field_value
        transform = transformations.get(field, lambda x: x)
        app.config[field] = transform(value)
    
    for field, value in default_configuration.iteritems():
        if field not in [f.field_name for f in all_config_fields]:
            app.config[field] = value
            new_cfg_field = ConfigurationField(field_name=field, field_value=value)
            db.session.add(new_cfg_field)
    db.session.commit()

def set_config_value(field, value):
    """Sets the configuration value specified in ``field`` to the value given in
    ``value``. ``value`` should be able to be converted to a string, as it is
    stored that way internally and transformed on the way out (see :func:load_config_from_db).

    :param field: The configuration field to change
    :type field: string
    :param value: The new value of ``field``
    :type value: string
    """
    config_field = ConfigurationField.query.filter_by(field_name=field).first()
    
    if config_field is None:
        config_field = ConfigurationField(field_name=field, field_value=value)
        db.session.add(config_field)
        db.session.commit()
    else:
        config_field.field_value = value
        
    db.session.commit()

def get_config_value(field):
    """Gets the value of ``field``.

    :param field: The configuration field to get
    :type field: string
    :returns: The value of the configuration field ``field``
    :rtype: String
    """
    config_field = ConfigurationField.query.filter_by(field_name=field).first()

    if config_field is not None:
        return config_field.field_value
    else:
        return None

def _produce_random_data():
    """Produces a SHA512 hash of the concatenation of 5000 random numbers (as a string).
    Used by :func:load_config_from_db to seed the ``SECRET_KEY`` and ``SESSION_SALT``
    configuration fields.

    :returns: A string of random data
    :rtype: string
    """
    m = hashlib.sha512()
    m.update(str(time.time()))
    for i in range(1,5000):
        m.update(str(random.random()))
    return m.hexdigest()
