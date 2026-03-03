from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewCreate(BaseModel):
    score: int
    body: Optional[str] = None
    spoiler: bool = False


class ReviewResponse(BaseModel):
    id: str
    user_id: str
    game_id: str
    score: int
    body: Optional[str] = None
    spoiler: bool
    created_at: datetime