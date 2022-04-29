import os

from sqlalchemy import (MetaData, create_engine)
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(
    DATABASE_URI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


