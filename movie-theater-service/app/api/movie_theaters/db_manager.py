from app.api.movie_theaters.models import (MovieTheaterIn, MovieTheaterOut, MovieTheaterUpdate)
from app.api.movie_theaters.db import theaters
from app.api.db import database

async def add_movie_theater(payload: MovieTheaterIn):
    query = theaters.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_movies_theater():
    query = theaters.select()
    return await database.fetch_all(query=query)

async def get_movie_theater(id):
    query = theaters.select(theaters.c.id==id)
    return await database.fetch_one(query=query)

async def delete_movie_theater(id: int):
    query = theaters.delete().where(theaters.c.id==id)
    return await database.execute(query=query)

async def update_movie_theater(id: int, payload: MovieTheaterIn):
    query = (
        theaters
        .update()
        .where(theaters.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)