from app.api.schemas import CastIn, CastOut, CastUpdate
from app.api.database import database
from app.api.models import casts


async def add_cast(payload: CastIn):
    query = casts.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_cast(id):
    query = casts.select(casts.c.id == id)
    return await database.fetch_one(query=query)


async def get_all_casts():
    query = casts.select()
    return await database.fetch_all(query=query)


async def update_cast(id: int, payload: CastIn):

    query = (
        casts
        .update()
        .where(casts.c.id == id)
        .values(**payload.dict())
    )

    await database.execute(query=query)

    query = casts.select(casts.c.id == id)
    return await database.fetch_one(query=query)
