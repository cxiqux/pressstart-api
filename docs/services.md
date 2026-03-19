# Services

Camada de lógica de negócio. Orquestra repositórios, aplica regras de domínio e lança exceções semânticas. Ficam em `app/services/`.

**Regra:** services nunca importam do FastAPI. Erros são `ValueError` ou `PermissionError` — as routes os traduzem em HTTP responses.

---

## `auth_service.py`

Gerencia autenticação e geração de tokens.

### `hash_password(password) → str`
Gera hash bcrypt da senha.

### `verify_password(plain, hashed) → bool`
Compara senha em texto plano com hash armazenado.

### `create_access_token(user_id) → str`
Cria JWT com payload `{sub, exp, type: "access"}`. Expira conforme `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.

### `create_refresh_token(user_id) → str`
Cria JWT com payload `{sub, exp, type: "refresh"}`. Expira conforme `JWT_REFRESH_TOKEN_EXPIRE_DAYS`.

### `register(username, email, password) → dict`
1. Verifica se e-mail já existe → `ValueError`
2. Verifica se username já existe → `ValueError`
3. Gera hash da senha
4. Cria usuário no banco
5. Retorna `TokenResponse`

### `login(email, password) → dict`
1. Busca usuário por e-mail
2. Se não encontrar ou senha errada → `ValueError("Credenciais inválidas")` (mensagem genérica intencional)
3. Retorna `TokenResponse`

### `refresh(refresh_token) → dict`
1. Decodifica e valida o JWT
2. Verifica que `type == "refresh"`
3. Busca usuário no banco
4. Retorna novos tokens (access + refresh)

---

## `user_service.py`

### `get_me(user) → dict`
Passa o dict do usuário adiante (vindo do `get_current_user`).

### `update_me(user_id, username, avatar_url) → dict`
1. Se `username` fornecido, verifica se já está em uso por outro usuário → `ValueError`
2. Chama `user_repository.update()`

### `get_public_profile(username) → dict`
1. Busca usuário por username
2. Se não encontrar → `ValueError`

---

## `game_service.py`

Integração com a **RAWG.io API** e cache local.

### `_parse_rawg_game(item) → dict`
Converte o formato da RAWG para o formato interno:
- `item["name"]` → `title`
- `item["background_image"]` → `cover_url`
- Primeiro gênero da lista → `genre`
- Primeira plataforma da lista → `platform`
- Ano extraído de `item["released"]` → `release_year`

### `search(query) → list`
1. Chama `GET /games` na RAWG com `search={query}&page_size=10`
2. Para cada resultado:
   - Se já existe em `games` (por `rawg_id`) → usa o cache
   - Se não → insere no banco
3. Retorna lista de até 10 jogos

### `get_game(game_id) → dict`
1. Busca jogo por UUID interno
2. Se não encontrar → `ValueError`

---

## `backlog_service.py`

### `list_backlog(user_id, status, sort, page) → list`
Repassa os filtros para `backlog_repository.get_all()`.

### `add_to_backlog(user_id, rawg_id, status, score, notes, hours_played) → dict`
1. Busca jogo por `rawg_id` no cache local
2. Se não existir → chama `game_service.search()` e localiza o jogo pelo `rawg_id`
3. Se ainda não encontrar → `ValueError`
4. Verifica duplicata (usuário + jogo) → `ValueError`
5. Cria entrada no backlog

### `update_entry(user_id, entry_id, ...) → dict`
1. Verifica ownership via `backlog_repository.get_owner()` → `ValueError` se não existe, `PermissionError` se não é dono
2. Chama `backlog_repository.update()`

### `delete_entry(user_id, entry_id) → None`
1. Verifica ownership → `ValueError` / `PermissionError`
2. Chama `backlog_repository.delete()`

---

## `review_service.py`

### `list_reviews(game_id) → list`
1. Verifica se o jogo existe → `ValueError`
2. Retorna `review_repository.get_by_game()`

### `create_review(user_id, game_id, score, body, spoiler) → dict`
Implementa as regras de negócio mais críticas da aplicação:

1. Verifica se o jogo existe → `ValueError`
2. Busca entrada no backlog do usuário para esse jogo
3. Se não existe ou status ≠ `done` → `ValueError("Só é possível avaliar jogos com status 'done' no backlog")`
4. Verifica se já existe review do usuário para esse jogo → `ValueError`
5. Cria a review

### `delete_review(user_id, review_id) → None`
1. Verifica ownership → `ValueError` / `PermissionError`
2. Chama `review_repository.delete()`
