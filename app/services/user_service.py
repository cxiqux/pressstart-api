from app.repositories import user_repository


def get_me(user: dict):
    return user


def update_me(user_id: str, username: str = None, avatar_url: str = None):
    if username is not None:
        existing = user_repository.get_by_username(username)
        if existing and str(existing["id"]) != user_id:
            raise ValueError("Username já em uso")

    return user_repository.update(user_id, username=username, avatar_url=avatar_url)


def get_public_profile(username: str):
    user = user_repository.get_by_username(username)
    if not user:
        raise ValueError("Usuário não encontrado")
    return user
