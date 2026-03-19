from app.core.database import get_connection

def get_by_email(email: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            return cursor.fetchone()
        
def get_by_username(username: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            return cursor.fetchone()
        
def create(username: str, email: str, password_hash: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.fetchone()
        
def get_by_id(user_id: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (user_id,)
            )
            return cursor.fetchone()


def update(user_id: str, username: str = None, avatar_url: str = None):
    fields = []
    values = []

    if username is not None:
        fields.append("username = %s")
        values.append(username)
    if avatar_url is not None:
        fields.append("avatar_url = %s")
        values.append(avatar_url)

    if not fields:
        return get_by_id(user_id)

    values.append(user_id)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET {', '.join(fields)} WHERE id = %s RETURNING *",
                values
            )
            conn.commit()
            return cursor.fetchone()