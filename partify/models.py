import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    username = Column(String(36), unique=True)
    password = Column(String(256))

    def __init__(self, name=None, username=None, password=None):
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User %r>" % (self.name)

class Track(Base):
    __tablename__ = "track"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    artist = Column(Text)
    album = Column(Text)
    spotify_url = Column(Text, unique=True)

    def __repr__(self):
        return "<%r by %r (from %r) - %r>" % (self.title, self.artist, self.album, self.spotify_url)

class PlayQueue(Base):
    __tablename__ = "play_queue"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    track_id = Column(Integer, ForeignKey('track.id'))
    track = relationship("Track")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")
    time_added = Column(DateTime, default=datetime.datetime.now)
    user_priority = Column(Integer)
    playback_priority = Column(BigInteger, unique=True)

    def __repr__(self):
        return "<Track %r queued by %r at %r with priority %r (queue position %r)>" % (self.track, self.user, self.time_added, self.user_priority, self.playback_priority)

class ConfigurationField(Base):
    __tablename__ = "configuration_field"

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_name = Column(Text)
    field_value = Column(Text)