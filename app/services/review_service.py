from app.repositories import review_repository, game_repository
from app.core.database import get_connection


def _get_backlog_entry(user_id: str, game_id: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT status FROM backlog_entries WHERE user_id = %s AND game_id = %s",
                (user_id, game_id),
            )
            return cursor.fetchone()


def list_reviews(game_id: str) -> list:
    game = game_repository.get_by_id(game_id)
    if not game:
        raise ValueError("Jogo não encontrado")
    return review_repository.get_by_game(game_id)


def create_review(user_id: str, game_id: str, score: int, body: str = None, spoiler: bool = False) -> dict:
    game = game_repository.get_by_id(game_id)
    if not game:
        raise ValueError("Jogo não encontrado")

    entry = _get_backlog_entry(user_id, game_id)
    if not entry or entry["status"] != "done":
        raise ValueError("Só é possível avaliar jogos com status 'done' no backlog")

    if review_repository.get_by_user_and_game(user_id, game_id):
        raise ValueError("Você já avaliou esse jogo")

    return review_repository.create(user_id, game_id, score, body, spoiler)


def delete_review(user_id: str, review_id: str) -> None:
    owner_id = review_repository.get_owner(review_id)
    if not owner_id:
        raise ValueError("Review não encontrada")
    if owner_id != user_id:
        raise PermissionError("Sem permissão")

    review_repository.delete(review_id)
