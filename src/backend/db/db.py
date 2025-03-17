import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
