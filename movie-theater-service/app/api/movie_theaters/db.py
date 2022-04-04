from sqlalchemy import (Column, Integer, String, Table, MetaData)

metadata = MetaData()

theaters = Table(
    'theaters',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50))
)
