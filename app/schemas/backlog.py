from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from app.schemas.game import GameResponse


class BacklogStatus(str, Enum):
    want = "want"
    playing = "playing"
    done = "done"
    dropped = "dropped"


class BacklogCreate(BaseModel):
    rawg_id: int
    status: BacklogStatus
    score: Optional[int] = None
    notes: Optional[str] = None
    hours_played: Optional[int] = None


class BacklogUpdate(BaseModel):
    status: Optional[BacklogStatus] = None
    score: Optional[int] = None
    notes: Optional[str] = None
    hours_played: Optional[int] = None


class BacklogResponse(BaseModel):
    id: str
    game_id: str
    game: GameResponse
    status: BacklogStatus
    score: Optional[int] = None
    notes: Optional[str] = None
    hours_played: Optional[int] = None
    updated_at: datetime