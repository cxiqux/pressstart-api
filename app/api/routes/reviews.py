from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services import review_service
from app.core.security import get_current_user

router = APIRouter(tags=["Reviews"])


@router.get("/games/{game_id}/reviews", response_model=List[ReviewResponse])
def list_reviews(game_id: str, current_user=Depends(get_current_user)):
    try:
        return review_service.list_reviews(game_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/games/{game_id}/reviews", response_model=ReviewResponse, status_code=201)
def create_review(game_id: str, body: ReviewCreate, current_user=Depends(get_current_user)):
    try:
        return review_service.create_review(
            str(current_user["id"]),
            game_id,
            score=body.score,
            body=body.body,
            spoiler=body.spoiler,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/reviews/{review_id}", status_code=204)
def delete_review(review_id: str, current_user=Depends(get_current_user)):
    try:
        review_service.delete_review(str(current_user["id"]), review_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
