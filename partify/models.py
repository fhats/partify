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

    def __init__(self, name=None, username=None, password=None):
        self.name = name
        self.username = username
        self.password = generate_password_hash(password)

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
        d['user_id'] = self.user_id
        return d


class ConfigurationField(db.Model):
    """Represents a configuration field."""
    __tablename__ = "configuration_field"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_name = db.Column(db.Text)
    field_value = db.Column(db.Text)
