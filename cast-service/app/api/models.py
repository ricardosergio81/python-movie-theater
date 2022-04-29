from app.api.database import Base
from sqlalchemy import (Column, Integer, String)


class Casts(Base):
    __tablename__ = "casts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    nationality = Column(String(20), index=True)

