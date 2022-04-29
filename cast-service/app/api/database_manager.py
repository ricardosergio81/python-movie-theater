from app.api.schemas import CastIn, CastOut, CastUpdate
from app.api.models import Casts
from sqlalchemy.orm import Session
from sqlalchemy import select,update


async def add_cast(db: Session, payload: CastIn):
    db_item = Casts(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


async def get_cast(db: Session, id: int) -> CastIn:
    items = select(Casts).where(Casts.id == id)
    response = db.execute(items).first()
    if response:
        return response[0]
    return False


async def get_all_casts(db: Session):
    items = select(Casts)
    return db.execute(items).scalars().all()


async def update_cast(db: Session, id: int, payload: CastIn):
    query = (
        update(Casts)
        .where(Casts.id == id)
        .values(name=payload.name)
    )

    db.execute(query)
    db.commit()
    db.refresh(payload)
    return payload
