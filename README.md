# 🎮 PressStart API

Backend da plataforma PressStart — seu backlog de jogos pessoal.

## Tecnologias

- **FastAPI** — framework web Python
- **PostgreSQL** — banco de dados relacional
- **SQLAlchemy** — ORM
- **Alembic** — migrations
- **JWT** — autenticação

## Requisitos

- Python 3.11+
- Docker Desktop

## Como rodar localmente

### 1. Clone o repositório
git clone https://github.com/cxiqux/pressstart-api.git
cd pressstart-api

### 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

### 3. Instale as dependências
pip install -r requirements.txt

### 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

### 5. Suba o banco de dados
docker compose up -d

### 6. Rode as migrations
alembic upgrade head

### 7. Inicie a aplicação
uvicorn app.main:app --reload

## Documentação da API

Com a aplicação rodando, acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estrutura do projeto

pressstart-api/
├── app/
│   ├── api/routes/     # Endpoints
│   ├── core/           # Config e database
│   ├── models/         # Tabelas do banco
│   ├── repositories/   # Queries
│   ├── schemas/        # Validação Pydantic
│   └── services/       # Lógica de negócio
├── alembic/            # Migrations
├── docker-compose.yml
├── requirements.txt
└── .env.example