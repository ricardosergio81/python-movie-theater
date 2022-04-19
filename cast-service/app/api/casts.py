from fastapi import APIRouter, HTTPException
from typing import List

from app.api.schemas import CastOut, CastIn, CastUpdate
from app.api import database_manager

casts = APIRouter()


@casts.post('/', response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn):
    cast_id = await database_manager.add_cast(payload)

    response = {
        'id': cast_id,
        **payload.dict()
    }

    return response


@casts.get('/', response_model=List[CastOut])
async def get_casts():
    return await database_manager.get_all_casts()


@casts.get('/{id}/', response_model=CastOut)
async def get_cast(id: int):
    cast = await database_manager.get_cast(id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast


@casts.put('/{id}/', response_model=CastOut)
async def update_cast(id: int, payload: CastUpdate):
    cast = await database_manager.get_cast(id)

    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")

    update_data = payload.dict(exclude_unset=True)

    cast_db = CastIn(**cast)

    updated_cast = cast_db.copy(update=update_data)

    return await database_manager.update_cast(id, updated_cast)