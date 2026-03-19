# PressStart API

Backend da plataforma PressStart — um backlog de jogos pessoal. Pensa num Letterboxd, mas para games. O usuário registra jogos que quer jogar, está jogando, terminou ou abandonou, dá notas, escreve reviews e vê o que seus amigos estão jogando.

## Stack

| Tecnologia | Uso |
|---|---|
| Python 3.13 + FastAPI 0.115 | Framework web e servidor |
| PostgreSQL 16 | Banco de dados |
| psycopg2-binary | Driver PostgreSQL (SQL puro, sem ORM) |
| Alembic 1.13 | Migrations |
| python-jose | JWT (HS256) |
| passlib + bcrypt 4.0.1 | Hash de senhas |
| pydantic[email] 2.9 + pydantic-settings 2.5 | Validação e configuração |
| httpx 0.27 | Chamadas HTTP para RAWG.io |

## Requisitos

- Python 3.13+
- Docker Desktop

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/cxiqux/pressstart-api.git
cd pressstart-api

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env

# 5. Suba o banco de dados
docker compose up -d

# 6. Rode as migrations
alembic upgrade head

# 7. Inicie a aplicação
uvicorn app.main:app --reload
```

API disponível em `http://localhost:8000`
Swagger UI em `http://localhost:8000/docs`
ReDoc em `http://localhost:8000/redoc`

## Endpoints

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | /auth/register | Cria conta e retorna tokens | — |
| POST | /auth/login | Autentica e retorna tokens | — |
| POST | /auth/refresh | Renova access token | — |
| GET | /users/me | Perfil do usuário autenticado | ✓ |
| PATCH | /users/me | Atualiza username e avatar | ✓ |
| GET | /users/{username} | Perfil público | ✓ |
| GET | /games/search?q= | Busca jogos na RAWG (com cache) | ✓ |
| GET | /games/{game_id} | Detalhes de um jogo | ✓ |
| GET | /backlog | Lista backlog com filtros | ✓ |
| POST | /backlog | Adiciona jogo ao backlog | ✓ |
| PATCH | /backlog/{entry_id} | Atualiza entrada do backlog | ✓ |
| DELETE | /backlog/{entry_id} | Remove do backlog | ✓ |
| GET | /games/{game_id}/reviews | Lista reviews públicas do jogo | ✓ |
| POST | /games/{game_id}/reviews | Publica review (requer status done) | ✓ |
| DELETE | /reviews/{review_id} | Remove review | ✓ |
| GET | /health | Health check | — |

## Estrutura do projeto

```
pressstart-api/
├── app/
│   ├── main.py                  # FastAPI instance e registro de routers
│   ├── core/
│   │   ├── config.py            # Pydantic Settings — lê .env
│   │   ├── database.py          # Conexão psycopg2
│   │   └── security.py          # Middleware JWT — get_current_user
│   ├── schemas/                 # Modelos Pydantic (request/response)
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── game.py
│   │   ├── backlog.py
│   │   └── review.py
│   ├── repositories/            # Queries SQL puras
│   │   ├── user_repository.py
│   │   ├── game_repository.py
│   │   ├── backlog_repository.py
│   │   └── review_repository.py
│   ├── services/                # Lógica de negócio
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── game_service.py
│   │   ├── backlog_service.py
│   │   └── review_service.py
│   └── api/routes/              # Endpoints FastAPI
│       ├── auth.py
│       ├── users.py
│       ├── games.py
│       ├── backlog.py
│       └── reviews.py
├── alembic/                     # Migrations
│   └── versions/
├── docs/                        # Documentação técnica
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
└── .env.example
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

```env
APP_NAME=PressStart
APP_ENV=development
SECRET_KEY=...
DATABASE_URL=postgresql://user:pass@localhost:5432/pressstart_db
JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30
RAWG_API_KEY=...
RAWG_BASE_URL=https://api.rawg.io/api
```

## Documentação técnica

Veja a pasta [`docs/`](docs/) para documentação detalhada de cada camada:

- [`docs/architecture.md`](docs/architecture.md) — Arquitetura e padrões
- [`docs/database.md`](docs/database.md) — Schema do banco de dados
- [`docs/core.md`](docs/core.md) — Config, database e security
- [`docs/schemas.md`](docs/schemas.md) — Modelos Pydantic
- [`docs/repositories.md`](docs/repositories.md) — Camada de acesso a dados
- [`docs/services.md`](docs/services.md) — Camada de negócio
- [`docs/api/`](docs/api/) — Documentação de cada grupo de endpoints
