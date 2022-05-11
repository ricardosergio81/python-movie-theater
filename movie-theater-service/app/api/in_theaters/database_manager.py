from app.api.in_theaters.schemas import (InTheatersIn, InTheatersOut, InTheatersUpdate)
from app.api.in_theaters.models import InTheaters
from sqlalchemy.orm import Session
from sqlalchemy import select, update


async def add_in_theater(db: Session, payload: InTheatersIn):
    db_item = InTheaters(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


async def get_all_in_theaters(db: Session):
    items = select(InTheaters)
    return db.execute(items).scalars().all()


async def get_in_theater(db: Session, id):
    items = select(InTheaters).where(InTheaters.id == id)
    response = db.execute(items).first()
    if response:
        return response[0]
    return False


async def update_in_theater(db: Session, id: int, payload: InTheatersIn):
    query = (
        update(InTheaters)
            .where(InTheaters.id == id)
            .values(theaters_id=payload.theaters_id,
                    movie_id=payload.movie_id,
                    day_of_week=payload.day_of_week,
                    time=payload.time,
                    exclude=payload.exclude
                    )
    )

    db.execute(query)
    db.commit()
    db.refresh(payload)
    return payload
