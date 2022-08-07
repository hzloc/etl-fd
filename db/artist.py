from unicodedata import name
from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    event_id = Column(Integer, ForeignKey('events.id'))

    def __init__(self, name):
        self.name = name