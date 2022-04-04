import os

from sqlalchemy import create_engine

from databases import Database
from app.api.movie_theaters.db import theaters, metadata
from app.api.in_theaters.db import in_theaters, metadata

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI, echo=True)

database = Database(DATABASE_URI)