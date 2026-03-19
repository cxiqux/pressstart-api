from app.repositories import backlog_repository, game_repository
from app.services import game_service


def list_backlog(user_id: str, status: str = None, sort: str = "updated_at", page: int = 1) -> list:
    return backlog_repository.get_all(user_id, status=status, sort=sort, page=page)


def add_to_backlog(user_id: str, rawg_id: int, status: str, score: int = None, notes: str = None, hours_played: int = None) -> dict:
    game = game_repository.get_by_rawg_id(rawg_id)
    if not game:
        results = game_service.search(str(rawg_id))
        game = next((g for g in results if g["rawg_id"] == rawg_id), None)
        if not game:
            raise ValueError("Jogo não encontrado na RAWG")

    game_id = str(game["id"])

    if backlog_repository.get_by_user_and_game(user_id, game_id):
        raise ValueError("Jogo já está no backlog")

    return backlog_repository.create(user_id, game_id, status, score, notes, hours_played)


def update_entry(user_id: str, entry_id: str, status: str = None, score: int = None, notes: str = None, hours_played: int = None) -> dict:
    owner_id = backlog_repository.get_owner(entry_id)
    if not owner_id:
        raise ValueError("Entrada não encontrada")
    if owner_id != user_id:
        raise PermissionError("Sem permissão")

    return backlog_repository.update(entry_id, status=status, score=score, notes=notes, hours_played=hours_played)


def delete_entry(user_id: str, entry_id: str) -> None:
    owner_id = backlog_repository.get_owner(entry_id)
    if not owner_id:
        raise ValueError("Entrada não encontrada")
    if owner_id != user_id:
        raise PermissionError("Sem permissão")

    backlog_repository.delete(entry_id)
