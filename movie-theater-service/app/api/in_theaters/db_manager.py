from app.api.in_theaters.models import (InTheatersIn, InTheatersOut, InTheatersUpdate)
from app.api.in_theaters.db import in_theaters
from app.api.db import database

async def add_in_theater(payload: InTheatersIn):
    query = in_theaters.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_in_theaters():
    query = in_theaters.select()
    return await database.fetch_all(query=query)

async def get_in_theater(id):
    query = in_theaters.select(in_theaters.c.id==id)
    return await database.fetch_one(query=query)

async def delete_in_theater(id: int):
    query = in_theaters.delete().where(in_theaters.c.id==id)
    return await database.execute(query=query)

async def update_in_theater(id: int, payload: InTheatersIn):
    query = (
        in_theaters
        .update()
        .where(in_theaters.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)