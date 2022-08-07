from msilib.schema import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    engine = create_engine('postgresql+psycopg2://root:password@localhost:5433/event')
except Error:
    print(Error)


Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
