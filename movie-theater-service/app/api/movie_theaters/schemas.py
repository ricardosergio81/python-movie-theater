from pydantic import BaseModel, Field
from typing import List, Optional


class MovieTheaterIn(BaseModel):
    name: str


class MovieTheaterOut(MovieTheaterIn):
    id: int

    class Config:
        orm_mode = True


class MovieTheaterUpdate(MovieTheaterIn):
    name: Optional[str] = None
