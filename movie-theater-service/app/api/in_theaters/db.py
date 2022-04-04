from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, ARRAY, Boolean, Time, MetaData)

metadata = MetaData()

in_theaters = Table(
    'in_theaters',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('theaters_id', Integer),
    Column('movie_id', Integer),
    Column('day_of_week', String),
    Column('time', Time),
    Column('exclude', Boolean),
)
