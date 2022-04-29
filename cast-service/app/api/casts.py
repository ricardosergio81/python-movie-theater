from fastapi import APIRouter, HTTPException
from typing import List
from app.api.schemas import CastOut, CastIn, CastUpdate
from app.api import database_manager
from app.api.database import SessionLocal

from fastapi import Depends
from sqlalchemy.orm import Session

casts = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@casts.post('/', response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn, db: Session = Depends(get_db)):
    return await database_manager.add_cast(db, payload)


@casts.get('/', response_model=List[CastOut])
async def get_casts(db: Session = Depends(get_db)):
    return await database_manager.get_all_casts(db)


@casts.get('/{id}/', response_model=CastOut)
async def get_cast(id: int, db: Session = Depends(get_db)):
    cast = await database_manager.get_cast(db, id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast


@casts.put('/{id}/', response_model=CastOut)
async def update_cast(id: int, payload: CastUpdate, db: Session = Depends(get_db)):
    cast = await database_manager.get_cast(db, id)

    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cast, key, value)

    return await database_manager.update_cast(db, id, cast)
