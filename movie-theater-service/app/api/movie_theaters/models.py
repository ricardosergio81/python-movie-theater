from app.api.database import Base
from sqlalchemy import (Column, Integer, String, Table, MetaData)


class Theaters(Base):
    __tablename__ = "theaters"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
