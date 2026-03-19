from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserResponse, UserUpdate
from app.services import user_service
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return user_service.get_me(current_user)


@router.patch("/me", response_model=UserResponse)
def update_me(body: UserUpdate, current_user=Depends(get_current_user)):
    try:
        return user_service.update_me(
            str(current_user["id"]),
            username=body.username,
            avatar_url=body.avatar_url,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{username}", response_model=UserResponse)
def get_user(username: str):
    try:
        return user_service.get_public_profile(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
