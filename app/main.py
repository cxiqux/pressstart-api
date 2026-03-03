from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}