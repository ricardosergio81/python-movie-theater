from typing import List
from fastapi import APIRouter, HTTPException

from app.api.in_theaters.models import (InTheatersIn, InTheatersOut, InTheatersUpdate)
from app.api.in_theaters import db_manager

from app.api.in_theaters.service import is_movie_theater_present, is_movie_present

inTheaters = APIRouter()

@inTheaters.post('/', response_model=InTheatersOut, status_code=201)
async def create_in_theater(payload: InTheatersIn):
    theater_id = payload.theaters_id
    if not is_movie_theater_present(theater_id):
        raise HTTPException(status_code=404, detail=f"Movie Theater with given id:{theater_id} not found")

    movies_id = payload.movie_id
    if not is_movie_present(movies_id):
        raise HTTPException(status_code=404, detail=f"Movie with given id:{movies_id} not found")

    movie_id = await db_manager.add_in_theater(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }

    return response

@inTheaters.get('/', response_model=List[InTheatersOut])
async def get_all_in_theater():
    return await db_manager.get_all_in_theaters()

@inTheaters.get('/{id}/', response_model=InTheatersOut)
async def get_in_theater(id: int):
    movie = await db_manager.get_in_theater(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@inTheaters.put('/{id}/', response_model=InTheatersOut)
async def update_in_theater(id: int, payload: InTheatersUpdate):
    movie = await db_manager.get_in_theater(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)
    movie_in_db = InTheaterIn(**movie)
    updated_movie = movie_in_db.copy(update=update_data)

    return await db_manager.update_in_theater(id, updated_movie)

@inTheaters.delete('/{id}/', response_model=None)
async def delete_in_theater(id: int):
    movie = await db_manager.get_in_theater(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await db_manager.delete_in_theater(id)
