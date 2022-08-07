from sqlalchemy import Column,Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from db.base import Base
from db.artist import Artist
from db.program import Program

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    event_date = Column(String)
    event_time = Column(String)
    event_location = Column(String)
    img_url = Column(String)
    artist = relationship(Artist, backref='events')
    program = relationship(Program, backref='events')

    def __init__(self, title, event_date, event_time, event_location, img_url):
        self.title = title
        self.event_date = event_date
        self.event_time = event_time
        self.event_location = event_location
        self.img_url = img_url