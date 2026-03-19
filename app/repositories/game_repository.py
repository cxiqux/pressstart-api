from app.core.database import get_connection


def get_by_rawg_id(rawg_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM games WHERE rawg_id = %s", (rawg_id,))
            return cursor.fetchone()


def get_by_id(game_id: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM games WHERE id = %s", (game_id,))
            return cursor.fetchone()


def create(rawg_id: int, title: str, cover_url: str = None, genre: str = None, platform: str = None, release_year: int = None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO games (rawg_id, title, cover_url, genre, platform, release_year)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (rawg_id, title, cover_url, genre, platform, release_year)
            )
            conn.commit()
            return cursor.fetchone()
