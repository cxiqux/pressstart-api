# Banco de Dados

## Configuração

- **SGBD:** PostgreSQL 16
- **Driver:** psycopg2-binary (SQL puro, sem ORM)
- **Migrations:** Alembic
- **Local:** Docker (`docker compose up -d`)
- **Produção:** Railway

## ENUMs

```sql
-- Status do jogo no backlog
CREATE TYPE backlog_status AS ENUM ('want', 'playing', 'done', 'dropped');

-- Status de amizade
CREATE TYPE friendship_status AS ENUM ('pending', 'accepted', 'blocked');
```

## Tabelas

### users

| Coluna | Tipo | Restrições |
|---|---|---|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() |
| username | VARCHAR(50) | NOT NULL, UNIQUE |
| email | VARCHAR(255) | NOT NULL, UNIQUE |
| password_hash | TEXT | NOT NULL |
| avatar_url | TEXT | — |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() |

> `password_hash` nunca é exposto em nenhum endpoint.

---

### games

Cache local dos dados vindos da RAWG.io. O backend popula essa tabela automaticamente na primeira busca.

| Coluna | Tipo | Restrições |
|---|---|---|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() |
| rawg_id | INTEGER | NOT NULL, UNIQUE |
| title | VARCHAR(255) | NOT NULL |
| cover_url | TEXT | — |
| genre | VARCHAR(100) | — |
| platform | VARCHAR(100) | — |
| release_year | SMALLINT | — |
| cached_at | TIMESTAMP | NOT NULL, DEFAULT NOW() |

---

### backlog_entries

| Coluna | Tipo | Restrições |
|---|---|---|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() |
| user_id | UUID | NOT NULL, FK → users(id) ON DELETE CASCADE |
| game_id | UUID | NOT NULL, FK → games(id) ON DELETE CASCADE |
| status | backlog_status | NOT NULL |
| score | SMALLINT | CHECK (score >= 1 AND score <= 10) |
| notes | TEXT | — |
| hours_played | INTEGER | — |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() |

**Constraint única:** `(user_id, game_id)` — um usuário não pode ter o mesmo jogo duas vezes.

---

### reviews

| Coluna | Tipo | Restrições |
|---|---|---|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() |
| user_id | UUID | NOT NULL, FK → users(id) ON DELETE CASCADE |
| game_id | UUID | NOT NULL, FK → games(id) ON DELETE CASCADE |
| score | SMALLINT | NOT NULL, CHECK (score >= 1 AND score <= 10) |
| body | TEXT | — |
| spoiler | BOOLEAN | NOT NULL, DEFAULT FALSE |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() |

**Constraint única:** `(user_id, game_id)` — um usuário só pode publicar uma review por jogo.
**Regra de negócio:** só é possível criar uma review se o jogo tiver status `done` no backlog do usuário.

---

### friendships

| Coluna | Tipo | Restrições |
|---|---|---|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() |
| requester_id | UUID | NOT NULL, FK → users(id) ON DELETE CASCADE |
| addressee_id | UUID | NOT NULL, FK → users(id) ON DELETE CASCADE |
| status | friendship_status | NOT NULL, DEFAULT 'pending' |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() |

**Constraint única:** `(requester_id, addressee_id)`

> Implementada via migration mas ainda não possui endpoints — será parte do micro-serviço Node.js (Fase 5).

---

## Relacionamentos

```
users ──< backlog_entries >── games
users ──< reviews >── games
users ──< friendships >── users
```

## Migrations

As migrations ficam em `alembic/versions/` e são aplicadas com:

```bash
alembic upgrade head    # aplica todas as migrations pendentes
alembic downgrade -1    # reverte a última migration
alembic history         # lista o histórico
```

Migrations existentes:
- `0d32083321e6` — create users table
- `85bcc899933e` — create games table
- `28147626d8eb` — create backlog_entries table
- `d14ba447a8a8` — create reviews table
- `c0580dbb5a32` — create friendships table
