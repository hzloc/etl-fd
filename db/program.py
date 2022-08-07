from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base


class Program(Base):
    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    event_id = Column(Integer, ForeignKey('events.id'))


    def __init__(self, title):
        self.title = title

