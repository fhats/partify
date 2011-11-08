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

import os
import os.path

from flaskext.sqlalchemy import SQLAlchemy

from partify import app

db_location = '../tmp/partify.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_location

# Uh... this is really ugly. :(
db_exists = True

if not os.path.exists(db_location):
    try:
        os.makedirs(os.path.split(db_location)[0])
    except:
        pass
    open(db_location, 'w+')
    db_exists = False

db = SQLAlchemy(app)

def init_db():
    import partify.models
    db.create_all()
    
def reinit_db():
    global db

    db = SQLAlchemy(app)
    db.create_all()

if not db_exists:
    init_db()

if __name__ == "__main__":
    init_db()