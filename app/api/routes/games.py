from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.game import GameResponse
from app.services import game_service
from app.core.security import get_current_user

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/search", response_model=List[GameResponse])
def search_games(q: str, current_user=Depends(get_current_user)):
    try:
        return game_service.search(q)
    except Exception:
        raise HTTPException(status_code=502, detail="Erro ao buscar jogos na RAWG")


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: str, current_user=Depends(get_current_user)):
    try:
        return game_service.get_game(game_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
