from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

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