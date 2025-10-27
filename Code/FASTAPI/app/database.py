from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/aiquest'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SeasionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SeasionLocal()
    try:
        yield db
    finally:
        db.close()