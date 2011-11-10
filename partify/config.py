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

import hashlib
import random
import time
from tempfile import mkstemp

from partify import app
from partify.database import db
from partify.models import ConfigurationField

def load_config_from_db():
    """Loads configuration fields from the database and throws them in the Partify config dict."""
    default_configuration = {
        'DEBUG': True,
        'LASTFM_API_KEY': '',
        'LASTFM_API_SECRET': '',
        'MPD_SERVER_HOSTNAME': '',
        'MPD_SERVER_PORT': 0,
        'PROFILE': False,
        'SECRET_KEY': _produce_random_data(),
        'SERVER': 'builtin',
        'SERVER_HOST': '0.0.0.0',
        'SERVER_PORT': 5000, 
        'SESSION_SALT': _produce_random_data()
    }

    # Transformations to be performed on the key in the DB in case it shouldn't be just a string
    transformations = {
        'DEBUG': lambda x: bool(int(x)),
        'MPD_SERVER_PORT': int,
        'PROFILE': lambda x: bool(int(x)),
        'SECRET_KEY': str,          # the secret key can't be unicode for some reason...
        'SERVER_PORT': int
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
            app.logger.warning("Adding field %s with value %s" % (field, value))
            new_cfg_field = ConfigurationField(field_name=field, field_value=value)
            db.session.add(new_cfg_field)
    db.session.commit()

def set_config_value(field, value):
    config_field = ConfigurationField.query.filter_by(field_name=field).first()
    
    if config_field is None:
        config_field = ConfigurationField(field_name=field, field_value=value)
        db.session.add(config_field)
        db.session.commit()
    else:
        config_field.field_value = value
    
    db.session.commit()

    app.logger.debug("Set configuration field %r to %r" % (field, value))

def get_config_value(field):
    config_field = ConfigurationField.query.filter_by(field_name=field).first()

    if config_field is not None:
        return config_field.field_value
    else:
        return None

def _produce_random_data():
    m = hashlib.sha512()
    m.update(str(time.time()))
    for i in range(1,5000):
            m.update(str(random.random()))
