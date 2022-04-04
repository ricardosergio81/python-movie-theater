from typing import List
from fastapi import APIRouter, HTTPException

from app.api.movie_theaters.models import (MovieTheaterIn, MovieTheaterOut, MovieTheaterUpdate)
from app.api.movie_theaters import db_manager

moviesTheaters = APIRouter()

@moviesTheaters.post('/', response_model=MovieTheaterOut, status_code=201)
async def create_movie(payload: MovieTheaterIn):
    movie_id = await db_manager.add_movie_theater(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }

    return response

@moviesTheaters.get('/', response_model=List[MovieTheaterOut])
async def get_movies():
    return await db_manager.get_all_movies_theater()

@moviesTheaters.get('/{id}/', response_model=MovieTheaterOut)
async def get_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@moviesTheaters.put('/{id}/', response_model=MovieTheaterOut)
async def update_movie(id: int, payload: MovieTheaterUpdate):
    movie = await db_manager.get_movie_theater(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)
    movie_in_db = MovieTheaterIn(**movie)
    updated_movie = movie_in_db.copy(update=update_data)

    return await db_manager.update_movie_theater(id, updated_movie)

@moviesTheaters.delete('/{id}/', response_model=None)
async def delete_movie(id: int):
    movie = await db_manager.get_movie_theater(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await db_manager.delete_movie_theater(id)
