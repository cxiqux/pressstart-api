# Repositories

Camada de acesso a dados. Toda query SQL da aplicação vive aqui. Ficam em `app/repositories/`.

Cada função abre sua própria conexão via `get_connection()`, executa a query e retorna um dict (ou lista de dicts) graças ao `RealDictCursor`. Nenhuma lógica de negócio aqui — só SQL.

---

## `user_repository.py`

| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `get_by_email` | `email: str` | dict \| None | Busca usuário por e-mail |
| `get_by_username` | `username: str` | dict \| None | Busca usuário por username |
| `get_by_id` | `user_id: str` | dict \| None | Busca usuário por UUID |
| `create` | `username, email, password_hash` | dict | Insere novo usuário, retorna a linha criada |
| `update` | `user_id, username=None, avatar_url=None` | dict | Atualiza campos fornecidos dinamicamente; se nenhum campo for passado, retorna o usuário sem alteração |

O `update` constrói o `SET` dinamicamente para só atualizar os campos não-nulos.

---

## `game_repository.py`

| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `get_by_rawg_id` | `rawg_id: int` | dict \| None | Busca jogo pelo ID externo da RAWG |
| `get_by_id` | `game_id: str` | dict \| None | Busca jogo pelo UUID interno |
| `create` | `rawg_id, title, cover_url, genre, platform, release_year` | dict | Insere jogo no cache local |

---

## `backlog_repository.py`

O repositório mais complexo. Usa um `JOIN` com `games` para popular os dados do jogo em todas as queries de listagem/busca.

### Helpers internos

- `_SORT_MAP` — mapeamento de string para cláusula `ORDER BY`:
  - `"updated_at"` → `be.updated_at DESC`
  - `"score"` → `be.score DESC NULLS LAST`
  - `"title"` → `g.title ASC`
- `_JOIN` — query base com `JOIN games`
- `_build_response(row)` — converte a linha flat do JOIN em dict aninhado com `game: {...}`

### Funções

| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `get_all` | `user_id, status=None, sort="updated_at", page=1, page_size=20` | list[dict] | Lista backlog com filtro, ordenação e paginação |
| `get_by_id` | `entry_id: str` | dict \| None | Busca entrada por UUID (com JOIN) |
| `get_by_user_and_game` | `user_id, game_id` | dict \| None | Verifica se usuário já tem o jogo no backlog |
| `get_owner` | `entry_id: str` | str \| None | Retorna o `user_id` dono da entrada (para ownership check) |
| `create` | `user_id, game_id, status, score, notes, hours_played` | dict | Cria entrada e retorna via `get_by_id` (com JOIN) |
| `update` | `entry_id, status, score, notes, hours_played` | dict | Atualiza campos dinamicamente + `updated_at = NOW()`, retorna via `get_by_id` |
| `delete` | `entry_id: str` | None | Remove entrada |

---

## `review_repository.py`

Usa JOIN com `users` para incluir `username` em todas as respostas.

### Helpers internos

- `_JOIN` — query base com `JOIN users`
- `_build_response(row)` — converte a linha flat em dict com `username` incluído

### Funções

| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `get_by_game` | `game_id: str` | list[dict] | Lista todas as reviews de um jogo, ordenadas por `created_at DESC` |
| `get_by_id` | `review_id: str` | dict \| None | Busca review por UUID (com JOIN) |
| `get_by_user_and_game` | `user_id, game_id` | dict \| None | Verifica se usuário já tem review do jogo |
| `get_owner` | `review_id: str` | str \| None | Retorna `user_id` dono da review |
| `create` | `user_id, game_id, score, body, spoiler` | dict | Cria review e retorna via `get_by_id` |
| `delete` | `review_id: str` | None | Remove review |
