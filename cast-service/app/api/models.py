from app.api.database import metadata
from sqlalchemy import (Column, Integer, String, Table)


casts = Table(
    'casts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('nationality', String(20))
)
