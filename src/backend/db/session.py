from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite3?check_same_thread=False')
engine.execute('PRAGMA foreign_keys = true;')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(engine)

def get():
    try:
        db_connection = engine.connect()
        db_session = Session(autocommit = False, autoflush = True, bind = db_connection)
        yield db_session
    finally:
        db_connection.close()
