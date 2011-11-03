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

"""Database->Python Class ORM mappings."""
import datetime

from werkzeug.security import generate_password_hash

from database import db

class User(db.Model):
    """Represents a User of Partify."""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(36), unique=True)
    password = db.Column(db.String(256))
    privs = db.Column(db.Integer)

    def __init__(self, name=None, username=None, password=None):
        self.name = name
        self.username = username
        self.password = generate_password_hash(password)
        self.privs = 0

    def __repr__(self):
        return "<User %r>" % (self.name)

class Track(db.Model):
    """Represents track metadata. Used as a foreign key in PlayQueueEntry."""
    __tablename__ = "track"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    artist = db.Column(db.Text)
    album = db.Column(db.Text)
    length = db.Column(db.Integer)
    date = db.Column(db.Text)
    spotify_url = db.Column(db.Text, unique=True)

    def __repr__(self):
        return "<%r by %r (from %r) - %r>" % (self.title, self.artist, self.album, self.spotify_url)
    
class PlayQueueEntry(db.Model):
    """Represents a playlist queue entry."""
    __tablename__ = "play_queue_entry"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    track = db.relationship("Track")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    mpd_id = db.Column(db.Integer)    # This SHOULD be unique... but since ensuring consistency isn't atomic yet we'll have to just best-effort it
    time_added = db.Column(db.DateTime, default=datetime.datetime.now)
    user_priority = db.Column(db.Integer, default=lambda: (db.session.query(db.func.max(PlayQueueEntry.user_priority)).first()[0] or 0) + 1)
    playback_priority = db.Column(db.BigInteger, default=lambda: (db.session.query(db.func.max(PlayQueueEntry.playback_priority)).first()[0] or 0) + 1)

    def __repr__(self):
        return "<Track %r (MPD %r) queued by %r at %r with priority %r (queue position %r)>" % (self.track, self.mpd_id, self.user, self.time_added, self.user_priority, self.playback_priority)

    def as_dict(self):
        # I'm not sure why a list comprehension into a dict doesn't work here...
        d = {}
        for attr in ('title', 'artist', 'album', 'spotify_url', 'date', 'length'):
            d[attr] = getattr(self.track, attr)
        for attr in ('id', 'mpd_id', 'playback_priority', 'user_priority'):
            d[attr] = getattr(self, attr)
        d['time_added'] = self.time_added.ctime()
        d['user'] = getattr(self.user, 'name', 'Anonymous')
        d['username'] = getattr(self.user, 'username', 'anonymous')
        d['user_id'] = self.user_id
        return d


class ConfigurationField(db.Model):
    """Represents a configuration field."""
    __tablename__ = "configuration_field"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_name = db.Column(db.Text)
    field_value = db.Column(db.Text)

    def __repr__(self):
        return "<ConfigurationField %r with value %r>" % (self.field_name, self.field_value)
