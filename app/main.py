from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, users, games, backlog, reviews


app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(games.router)
app.include_router(backlog.router)
app.include_router(reviews.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}