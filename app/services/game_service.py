import httpx
from app.core.config import settings
from app.repositories import game_repository


def _parse_rawg_game(item: dict) -> dict:
    genre = item["genres"][0]["name"] if item.get("genres") else None
    platform = item["platforms"][0]["platform"]["name"] if item.get("platforms") else None
    release_year = int(item["released"][:4]) if item.get("released") else None
    return {
        "rawg_id": item["id"],
        "title": item["name"],
        "cover_url": item.get("background_image"),
        "genre": genre,
        "platform": platform,
        "release_year": release_year,
    }


def search(query: str) -> list:
    with httpx.Client(timeout=10) as client:
        response = client.get(
            f"{settings.RAWG_BASE_URL}/games",
            params={"key": settings.RAWG_API_KEY, "search": query, "page_size": 10},
        )
        response.raise_for_status()

    results = response.json().get("results", [])
    games = []
    for item in results:
        parsed = _parse_rawg_game(item)
        existing = game_repository.get_by_rawg_id(parsed["rawg_id"])
        games.append(existing if existing else game_repository.create(**parsed))

    return games


def get_game(game_id: str):
    game = game_repository.get_by_id(game_id)
    if not game:
        raise ValueError("Jogo não encontrado")
    return game
