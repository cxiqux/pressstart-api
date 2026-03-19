from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from app.repositories import user_repository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": user_id, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def register(username: str, email: str, password: str):
    if user_repository.get_by_email(email):
        raise ValueError("Email já cadastrado")

    if user_repository.get_by_username(username):
        raise ValueError("Username já cadastrado")

    password_hash = hash_password(password)
    user = user_repository.create(username, email, password_hash)

    return {
        "access_token": create_access_token(str(user["id"])),
        "refresh_token": create_refresh_token(str(user["id"])),
        "token_type": "bearer"
    }


def login(email: str, password: str):
    user = user_repository.get_by_email(email)

    if not user or not verify_password(password, user["password_hash"]):
        raise ValueError("Credenciais inválidas")

    return {
        "access_token": create_access_token(str(user["id"])),
        "refresh_token": create_refresh_token(str(user["id"])),
        "token_type": "bearer"
    }


def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise ValueError("Token inválido")
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token inválido")
    except JWTError:
        raise ValueError("Token inválido")

    user = user_repository.get_by_id(user_id)
    if not user:
        raise ValueError("Usuário não encontrado")

    return {
        "access_token": create_access_token(str(user["id"])),
        "refresh_token": create_refresh_token(str(user["id"])),
        "token_type": "bearer"
    }