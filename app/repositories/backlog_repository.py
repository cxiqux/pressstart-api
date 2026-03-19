from app.core.database import get_connection

_SORT_MAP = {
    "updated_at": "be.updated_at DESC",
    "score": "be.score DESC NULLS LAST",
    "title": "g.title ASC",
}

_JOIN = """
    SELECT
        be.id, be.game_id, be.status, be.score, be.notes, be.hours_played, be.updated_at,
        g.id AS g_id, g.rawg_id, g.title, g.cover_url, g.genre, g.platform, g.release_year, g.cached_at
    FROM backlog_entries be
    JOIN games g ON g.id = be.game_id
"""


def _build_response(row: dict) -> dict:
    return {
        "id": str(row["id"]),
        "game_id": str(row["game_id"]),
        "game": {
            "id": str(row["g_id"]),
            "rawg_id": row["rawg_id"],
            "title": row["title"],
            "cover_url": row["cover_url"],
            "genre": row["genre"],
            "platform": row["platform"],
            "release_year": row["release_year"],
            "cached_at": row["cached_at"],
        },
        "status": row["status"],
        "score": row["score"],
        "notes": row["notes"],
        "hours_played": row["hours_played"],
        "updated_at": row["updated_at"],
    }


def get_all(user_id: str, status: str = None, sort: str = "updated_at", page: int = 1, page_size: int = 20) -> list:
    order = _SORT_MAP.get(sort, _SORT_MAP["updated_at"])
    offset = (page - 1) * page_size

    where = "WHERE be.user_id = %s"
    params = [user_id]

    if status:
        where += " AND be.status = %s"
        params.append(status)

    params += [page_size, offset]

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"{_JOIN} {where} ORDER BY {order} LIMIT %s OFFSET %s",
                params,
            )
            return [_build_response(row) for row in cursor.fetchall()]


def get_by_id(entry_id: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"{_JOIN} WHERE be.id = %s", (entry_id,))
            row = cursor.fetchone()
            return _build_response(row) if row else None


def get_by_user_and_game(user_id: str, game_id: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM backlog_entries WHERE user_id = %s AND game_id = %s",
                (user_id, game_id),
            )
            return cursor.fetchone()


def create(user_id: str, game_id: str, status: str, score: int = None, notes: str = None, hours_played: int = None) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO backlog_entries (user_id, game_id, status, score, notes, hours_played)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (user_id, game_id, status, score, notes, hours_played),
            )
            conn.commit()
            entry_id = cursor.fetchone()["id"]
    return get_by_id(str(entry_id))


def update(entry_id: str, status: str = None, score: int = None, notes: str = None, hours_played: int = None) -> dict:
    fields = []
    values = []

    if status is not None:
        fields.append("status = %s")
        values.append(status)
    if score is not None:
        fields.append("score = %s")
        values.append(score)
    if notes is not None:
        fields.append("notes = %s")
        values.append(notes)
    if hours_played is not None:
        fields.append("hours_played = %s")
        values.append(hours_played)

    if not fields:
        return get_by_id(entry_id)

    fields.append("updated_at = NOW()")
    values.append(entry_id)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE backlog_entries SET {', '.join(fields)} WHERE id = %s",
                values,
            )
            conn.commit()

    return get_by_id(entry_id)


def delete(entry_id: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM backlog_entries WHERE id = %s", (entry_id,))
            conn.commit()


def get_owner(entry_id: str) -> str | None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id FROM backlog_entries WHERE id = %s", (entry_id,))
            row = cursor.fetchone()
            return str(row["user_id"]) if row else None
