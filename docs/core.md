# Core

Infraestrutura compartilhada da aplicação. Nenhuma outra camada além do `core` deve lidar com configuração, conexão com banco ou autenticação.

---

## `app/core/config.py`

Carrega e valida as variáveis de ambiente usando **pydantic-settings**.

```python
settings = Settings()  # singleton importado por toda a aplicação
```

| Variável | Tipo | Descrição |
|---|---|---|
| `APP_NAME` | str | Nome da aplicação |
| `APP_ENV` | str | `development`, `production` ou `testing` |
| `SECRET_KEY` | str | Chave geral da aplicação |
| `DATABASE_URL` | str | Connection string PostgreSQL |
| `JWT_SECRET_KEY` | str | Chave para assinar tokens JWT |
| `JWT_ALGORITHM` | str | Algoritmo JWT (padrão: `HS256`) |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | int | Expiração do access token (padrão: 60) |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | int | Expiração do refresh token (padrão: 30) |
| `RAWG_API_KEY` | str | Chave da API RAWG.io |
| `RAWG_BASE_URL` | str | URL base da RAWG (`https://api.rawg.io/api`) |

`APP_ENV` é validado via `@field_validator` — lança erro se o valor não for um dos três permitidos.

---

## `app/core/database.py`

Gerencia a conexão com o PostgreSQL via **psycopg2**.

### `get_connection()`
Retorna uma conexão psycopg2 com `RealDictCursor` como cursor padrão.

- `RealDictCursor` faz as linhas retornadas serem dicts (`row["coluna"]`) em vez de tuplas
- Usado nos repositories com `with get_connection() as conn:`
- A conexão não é fechada automaticamente pelo context manager do psycopg2 — o `with` gerencia apenas a transação (commit/rollback)

### `get_db()`
Generator para injeção de dependência via FastAPI (`Depends(get_db)`).

- Abre conexão, faz commit ao final, rollback em caso de exceção, fecha a conexão
- Disponível para uso futuro nas routes, mas os repositories atualmente gerenciam a própria conexão

---

## `app/core/security.py`

Middleware de autenticação JWT. Expõe a dependência `get_current_user` usada em todas as rotas protegidas.

### `get_current_user(credentials)`

**Dependência FastAPI** — injetada via `Depends(get_current_user)` nas routes.

Fluxo:
1. Extrai o Bearer token do header `Authorization`
2. Decodifica e valida o JWT com `JWT_SECRET_KEY` e `JWT_ALGORITHM`
3. Verifica que o payload tem `type: "access"` (rejeita refresh tokens)
4. Busca o usuário pelo `sub` (user_id) no banco
5. Retorna o dict do usuário — disponível nas routes como `current_user`

Erros retornados:
- `401` — token inválido, expirado ou mal formado
- `401` — usuário não encontrado no banco
