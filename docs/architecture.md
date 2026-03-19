# Arquitetura

## Visão geral

O PressStart API segue uma **arquitetura em camadas** com fluxo unidirecional de dependências:

```
Request → Routes → Services → Repositories → PostgreSQL
```

Cada camada tem uma responsabilidade única e só pode depender da camada imediatamente abaixo dela.

## Camadas

### Routes (`app/api/routes/`)
Responsabilidade: receber a requisição HTTP, validar via schema Pydantic, chamar o service e retornar a response.

- Não contém lógica de negócio
- Não faz queries SQL
- Traduz exceções (`ValueError` → 400/404, `PermissionError` → 403) em respostas HTTP

### Services (`app/services/`)
Responsabilidade: lógica de negócio, orquestração e regras de domínio.

- Decide o que fazer com os dados
- Pode chamar múltiplos repositories
- Lança exceções semânticas (`ValueError`, `PermissionError`) — nunca HTTPException
- É testável isoladamente

### Repositories (`app/repositories/`)
Responsabilidade: acesso ao banco de dados. SQL puro via psycopg2.

- Não contém lógica de negócio
- Retorna dicts (via `RealDictCursor`)
- Cada função representa uma query específica

### Schemas (`app/schemas/`)
Modelos Pydantic usados em dois sentidos:
- **Input** (Request body): validação automática pelo FastAPI
- **Output** (Response model): serialização e filtragem dos dados retornados

### Core (`app/core/`)
Infraestrutura compartilhada: configuração, conexão com banco e middleware de autenticação.

## Padrões adotados

| Padrão | Decisão |
|---|---|
| ORM | Não usado. SQL puro com psycopg2 + RealDictCursor |
| Autenticação | JWT Bearer (HS256). Access token (60 min) + Refresh token (30 dias) |
| Serialização | Pydantic v2 com `model_config` |
| Variáveis de ambiente | pydantic-settings lendo `.env` |
| API externa | RAWG.io proxiada pelo backend — o frontend nunca chama a RAWG diretamente |
| Cache de jogos | Jogos da RAWG são salvos na tabela `games` na primeira busca |

## Estrutura de pastas

```
app/
├── main.py                  # Ponto de entrada — FastAPI instance, routers
├── core/
│   ├── config.py            # Settings via pydantic-settings
│   ├── database.py          # get_connection() e get_db()
│   └── security.py          # Dependency get_current_user
├── schemas/
│   ├── auth.py              # TokenResponse, RefreshRequest
│   ├── user.py              # UserCreate, UserResponse, UserUpdate
│   ├── game.py              # GameResponse
│   ├── backlog.py           # BacklogCreate, BacklogUpdate, BacklogResponse, BacklogStatus
│   └── review.py            # ReviewCreate, ReviewResponse
├── repositories/
│   ├── user_repository.py
│   ├── game_repository.py
│   ├── backlog_repository.py
│   └── review_repository.py
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   ├── game_service.py
│   ├── backlog_service.py
│   └── review_service.py
└── api/
    └── routes/
        ├── auth.py
        ├── users.py
        ├── games.py
        ├── backlog.py
        └── reviews.py
```

## Fluxo de uma requisição típica

Exemplo: `POST /backlog` (adicionar jogo ao backlog)

1. **Route** recebe o body, valida com `BacklogCreate`, extrai `current_user` via `get_current_user`
2. **Service** (`backlog_service.add_to_backlog`):
   - Consulta `game_repository.get_by_rawg_id()` — jogo está no cache?
   - Se não, chama `game_service.search()` que busca na RAWG e salva no banco
   - Verifica se o usuário já tem o jogo no backlog (`backlog_repository.get_by_user_and_game`)
   - Cria a entrada (`backlog_repository.create`)
3. **Repository** executa o `INSERT` e retorna a entrada via JOIN com `games`
4. **Route** retorna o dict validado pelo `BacklogResponse`
