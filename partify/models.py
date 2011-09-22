"""Database->Python Class ORM mappings."""
import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database import Base
from database import db_session

class User(Base):
    """Represents a User of Partify."""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    username = Column(String(36), unique=True)
    password = Column(String(256))  # TODO: This needs to be encrypted. See issue #3 (https://github.com/fxh32/partify/issues/3)

    def __init__(self, name=None, username=None, password=None):
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User %r>" % (self.name)

class Track(Base):
    """Represents track metadata. Used as a foreign key in PlayQueueEntry."""
    __tablename__ = "track"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    artist = Column(Text)
    album = Column(Text)
    spotify_url = Column(Text, unique=True)

    def __repr__(self):
        return "<%r by %r (from %r) - %r>" % (self.title, self.artist, self.album, self.spotify_url)

class PlayQueueEntry(Base):
    """Represents a playlist queue entry."""
    __tablename__ = "play_queue_entry"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    track_id = Column(Integer, ForeignKey('track.id'))
    track = relationship("Track")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")
    mpd_id = Column(Integer, unique=True)
    time_added = Column(DateTime, default=datetime.datetime.now)
    user_priority = Column(Integer, default=lambda: (db_session.query(func.max(PlayQueueEntry.user_priority)).first()[0] or 0) + 1)
    playback_priority = Column(BigInteger, default=lambda: (db_session.query(func.max(PlayQueueEntry.playback_priority)).first()[0] or 0) + 1)

    def __repr__(self):
        return "<Track %r (MPD %r) queued by %r at %r with priority %r (queue position %r)>" % (self.track, self.mpd_id, self.user, self.time_added, self.user_priority, self.playback_priority)

class ConfigurationField(Base):
    """Represents a configuration field."""
    __tablename__ = "configuration_field"

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_name = Column(Text)
    field_value = Column(Text)
