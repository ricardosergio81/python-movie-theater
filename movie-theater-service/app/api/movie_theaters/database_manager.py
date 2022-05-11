from app.api.movie_theaters.schemas import (MovieTheaterIn, MovieTheaterOut, MovieTheaterUpdate)
from app.api.movie_theaters.models import Theaters
from sqlalchemy.orm import Session
from sqlalchemy import select, update


async def add_movie_theater(db: Session, payload: MovieTheaterIn):
    db_item = Theaters(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


async def get_all_movies_theater(db: Session):
    items = select(Theaters)
    return db.execute(items).scalars().all()


async def get_movie_theater(db: Session, id) -> MovieTheaterIn:
    items = select(Theaters).where(Theaters.id == id)
    response = db.execute(items).first()
    if response:
        return response[0]
    return False


async def update_movie_theater(db: Session, id: int, payload: MovieTheaterIn):
    query = (
        update(Theaters)
            .where(Theaters.id == id)
            .values(name=payload.name)
    )

    db.execute(query)
    db.commit()
    db.refresh(payload)
    return payload
