from app.api.schemas import MovieIn, MovieOut, MovieUpdate
from app.api.models import Movies
from sqlalchemy.orm import Session
from sqlalchemy import select, update


async def add_movie(db: Session, payload: MovieIn):
    db_item = Movies(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


async def get_all_movies(db: Session):
    items = select(Movies)
    return db.execute(items).scalars().all()


async def get_movie(db: Session, id: int):
    items = select(Movies).where(Movies.id == id)
    response = db.execute(items).first()
    if response:
        return response[0]
    return False


#
# async def delete_movie(db: Session,id: int):
#     query = movies.delete().where(movies.c.id == id)
#     return await database.execute(query=query)
#
#

async def update_movie(db: Session, id: int, payload: MovieIn):
    query = (
        update(Movies)
            .where(Movies.id == id)
            .values(name=payload.name,
                    plot=payload.plot,
                    genres=payload.genres,
                    casts_id=payload.casts_id,
                    year=payload.year)
    )

    db.execute(query)
    db.commit()
    db.refresh(payload)
    return payload
