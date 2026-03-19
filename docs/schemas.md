# Schemas

Modelos Pydantic que definem o contrato da API — validação de entrada e serialização de saída. Ficam em `app/schemas/`.

Padrão adotado: `model_config` em vez de `class Config` (Pydantic v2).

---

## `auth.py`

### `TokenResponse`
Retornado em todos os endpoints de autenticação.

| Campo | Tipo | Descrição |
|---|---|---|
| `access_token` | str | JWT de acesso (expira em 60 min) |
| `refresh_token` | str | JWT de renovação (expira em 30 dias) |
| `token_type` | str | Sempre `"bearer"` |

### `RefreshRequest`
Body do `POST /auth/refresh`.

| Campo | Tipo |
|---|---|
| `refresh_token` | str |

---

## `user.py`

### `UserCreate`
Body do `POST /auth/register` e `POST /auth/login`.

| Campo | Tipo | Validação |
|---|---|---|
| `username` | str | — |
| `email` | EmailStr | formato de e-mail |
| `password` | str | — |

### `UserResponse`
Retornado em todos os endpoints de usuário. **Nunca expõe `password_hash`.**

| Campo | Tipo |
|---|---|
| `id` | str (UUID) |
| `username` | str |
| `email` | EmailStr |
| `avatar_url` | str \| None |
| `created_at` | datetime |

### `UserUpdate`
Body do `PATCH /users/me`. Todos os campos são opcionais.

| Campo | Tipo |
|---|---|
| `username` | str \| None |
| `avatar_url` | str \| None |

---

## `game.py`

### `GameResponse`
Retornado em buscas de jogos e aninhado em `BacklogResponse`.

| Campo | Tipo |
|---|---|
| `id` | str (UUID) |
| `rawg_id` | int |
| `title` | str |
| `cover_url` | str \| None |
| `genre` | str \| None |
| `platform` | str \| None |
| `release_year` | int \| None |
| `cached_at` | datetime |

---

## `backlog.py`

### `BacklogStatus`
Enum com os status possíveis de um jogo no backlog:

| Valor | Significado |
|---|---|
| `want` | Quer jogar |
| `playing` | Jogando atualmente |
| `done` | Terminou |
| `dropped` | Abandonou |

### `BacklogCreate`
Body do `POST /backlog`.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `rawg_id` | int | ✓ |
| `status` | BacklogStatus | ✓ |
| `score` | int \| None | — |
| `notes` | str \| None | — |
| `hours_played` | int \| None | — |

### `BacklogUpdate`
Body do `PATCH /backlog/{entry_id}`. Todos opcionais.

| Campo | Tipo |
|---|---|
| `status` | BacklogStatus \| None |
| `score` | int \| None |
| `notes` | str \| None |
| `hours_played` | int \| None |

### `BacklogResponse`
Retornado nas listagens e operações de backlog. Inclui dados completos do jogo aninhados.

| Campo | Tipo |
|---|---|
| `id` | str (UUID) |
| `game_id` | str (UUID) |
| `game` | GameResponse |
| `status` | BacklogStatus |
| `score` | int \| None |
| `notes` | str \| None |
| `hours_played` | int \| None |
| `updated_at` | datetime |

---

## `review.py`

### `ReviewCreate`
Body do `POST /games/{game_id}/reviews`.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `score` | int | ✓ |
| `body` | str \| None | — |
| `spoiler` | bool | — (padrão: `false`) |

### `ReviewResponse`
Retornado nas listagens e criação de reviews. Inclui o username do autor.

| Campo | Tipo |
|---|---|
| `id` | str (UUID) |
| `user_id` | str (UUID) |
| `username` | str |
| `game_id` | str (UUID) |
| `score` | int |
| `body` | str \| None |
| `spoiler` | bool |
| `created_at` | datetime |
