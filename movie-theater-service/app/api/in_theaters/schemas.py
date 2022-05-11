from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import time


class InTheatersIn(BaseModel):
    theaters_id: int
    movie_id: int
    day_of_week: str
    time: time
    exclude: bool = False


class InTheatersOut(InTheatersIn):
    id: int

    class Config:
        orm_mode = True


class InTheatersUpdate(InTheatersIn):
    theaters_id: Optional[int] = None
    movie_id: Optional[int] = None
    day_of_week: Optional[str] = None
    time: Optional[time] = None
    exclude: Optional[bool] = None
