from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse, RefreshRequest
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(body: UserCreate):
    try:
        return auth_service.register(body.username, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(body: UserCreate):
    try:
        return auth_service.login(body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest):
    try:
        return auth_service.refresh(body.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))