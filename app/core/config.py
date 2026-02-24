from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    APP_NAME: str = "PressStart"
    APP_ENV: str = "development"
    SECRET_KEY: str

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    RAWG_API_KEY: str
    RAWG_BASE_URL: str = "https://api.rawg.io/api"

    @field_validator("APP_ENV")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        if v not in ("development", "production", "testing"):
            raise ValueError(f"APP_ENV must be one of: development, production, testing")
        return v

    model_config = {"env_file": ".env", "case_sensitive": True}

settings = Settings()