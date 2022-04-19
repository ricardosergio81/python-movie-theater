from pydantic import BaseModel
from typing import Optional


class CastIn(BaseModel):
    name: str
    nationality: Optional[str] = None


class CastOut(CastIn):
    id: int


class CastUpdate(CastIn):
    name: Optional[str] = None
    nationality: Optional[str] = None
