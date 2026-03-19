from app.core.database import get_connection

_JOIN = """
    SELECT
        r.id, r.user_id, r.game_id, r.score, r.body, r.spoiler, r.created_at,
        u.username
    FROM reviews r
    JOIN users u ON u.id = r.user_id
"""


def _build_response(row: dict) -> dict:
    return {
        "id": str(row["id"]),
        "user_id": str(row["user_id"]),
        "username": row["username"],
        "game_id": str(row["game_id"]),
        "score": row["score"],
        "body": row["body"],
        "spoiler": row["spoiler"],
        "created_at": row["created_at"],
    }


def get_by_game(game_id: str) -> list:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"{_JOIN} WHERE r.game_id = %s ORDER BY r.created_at DESC",
                (game_id,),
            )
            return [_build_response(row) for row in cursor.fetchall()]


def get_by_id(review_id: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"{_JOIN} WHERE r.id = %s", (review_id,))
            row = cursor.fetchone()
            return _build_response(row) if row else None


def get_by_user_and_game(user_id: str, game_id: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM reviews WHERE user_id = %s AND game_id = %s",
                (user_id, game_id),
            )
            return cursor.fetchone()


def get_owner(review_id: str) -> str | None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id FROM reviews WHERE id = %s", (review_id,))
            row = cursor.fetchone()
            return str(row["user_id"]) if row else None


def create(user_id: str, game_id: str, score: int, body: str = None, spoiler: bool = False) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO reviews (user_id, game_id, score, body, spoiler)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (user_id, game_id, score, body, spoiler),
            )
            conn.commit()
            review_id = cursor.fetchone()["id"]
    return get_by_id(str(review_id))


def delete(review_id: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
            conn.commit()
