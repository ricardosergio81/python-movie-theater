from app.api.database import Base
from sqlalchemy import (Column, Integer, String, ARRAY)


class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    plot = Column(String(250))
    genres = Column(ARRAY(String))
    casts_id = Column(ARRAY(Integer))
    year = Column(Integer)
