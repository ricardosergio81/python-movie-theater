from typing import List
from fastapi import APIRouter, HTTPException

from app.api.schemas import MovieOut, MovieIn, MovieUpdate
from app.api import database_manager
from app.api.service import is_cast_present
from app.api.database import SessionLocal

from fastapi import Depends
from sqlalchemy.orm import Session

movies = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@movies.post('/', response_model=MovieOut, status_code=201)
async def create_cast(payload: MovieIn, db: Session = Depends(get_db)):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    return await database_manager.add_movie(db, payload)


@movies.get('/', response_model=List[MovieOut])
async def get_movies(db: Session = Depends(get_db)):
    return await database_manager.get_all_movies(db)


@movies.get('/{id}/', response_model=MovieOut)
async def get_movie(id: int, db: Session = Depends(get_db)):
    movie = await database_manager.get_movie(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@movies.put('/{id}/', response_model=MovieOut)
async def update_movie(id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    movie = await database_manager.get_movie(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    for key, value in update_data.items():
        setattr(movie, key, value)

    return await database_manager.update_movie(db, id, movie)


@movies.delete('/{id}/', response_model=None)
async def delete_movie(id: int, db: Session = Depends(get_db)):
    movie = await database_manager.get_movie(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await database_manager.delete_movie(db, id)
