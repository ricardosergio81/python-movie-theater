from typing import List
from fastapi import APIRouter, HTTPException

from app.api.movie_theaters.schemas import (MovieTheaterIn, MovieTheaterOut, MovieTheaterUpdate)
from app.api.movie_theaters import database_manager

from fastapi import Depends
from sqlalchemy.orm import Session
from app.api.database import SessionLocal

moviesTheaters = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@moviesTheaters.post('/', response_model=MovieTheaterOut, status_code=201)
async def create_movie(payload: MovieTheaterIn, db: Session = Depends(get_db)):
    return await database_manager.add_movie_theater(db, payload)


@moviesTheaters.get('/', response_model=List[MovieTheaterOut])
async def get_movies(db: Session = Depends(get_db)):
    return await database_manager.get_all_movies_theater(db)


@moviesTheaters.get('/{id}/', response_model=MovieTheaterOut)
async def get_movie(id: int, db: Session = Depends(get_db)):
    movie = await database_manager.get_movie_theater(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@moviesTheaters.put('/{id}/', response_model=MovieTheaterOut)
async def update_movie(id: int, payload: MovieTheaterUpdate, db: Session = Depends(get_db)):
    movie = await database_manager.get_movie_theater(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(movie, key, value)

    return await database_manager.update_movie_theater(db, id, movie)

# @moviesTheaters.delete('/{id}/', response_model=None)
# async def delete_movie(id: int, db: Session = Depends(get_db)):
#     movie = await database_manager.get_movie_theater(id)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     return await database_manager.delete_movie_theater(id)
