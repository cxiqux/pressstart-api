from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GameResponse(BaseModel):
    id: str
    rawg_id : int
    title: str
    cover_url: Optional[str] = None
    genre: Optional[str] = None
    platform: Optional[str] = None
    release_year: Optional[int] = None
    cached_at: datetime
