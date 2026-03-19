# API — Games

Endpoints de jogos. Todos requerem autenticação Bearer.

O frontend **nunca** chama a RAWG diretamente — todas as buscas passam por esses endpoints, que fazem cache automático no banco.

Prefix: `/games` | Tag: `Games`

---

## GET /games/search

Busca jogos pelo nome. Consulta a RAWG.io e armazena os resultados no banco local na primeira vez.

**Query params**

| Param | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `q` | string | ✓ | Termo de busca |

**Exemplo:** `GET /games/search?q=hollow+knight`

**Response `200`** — lista de até 10 jogos
```json
[
  {
    "id": "9ff5774e-d45b-4f82-83c3-f490362196d2",
    "rawg_id": 9767,
    "title": "Hollow Knight",
    "cover_url": "https://media.rawg.io/media/games/4cf/...",
    "genre": "Platformer",
    "platform": "PC",
    "release_year": 2017,
    "cached_at": "2026-03-19T21:56:13.015292"
  }
]
```

**Comportamento de cache:**
- Se o jogo já existe no banco (por `rawg_id`), retorna do cache sem chamar a RAWG
- Se não existe, insere no banco e retorna
- O `cached_at` não é atualizado em buscas subsequentes

**Erros**
| Status | Motivo |
|---|---|
| 502 | Falha na comunicação com a RAWG |

---

## GET /games/{game_id}

Retorna os detalhes de um jogo pelo UUID interno (não pelo rawg_id).

**Response `200`**
```json
{
  "id": "9ff5774e-d45b-4f82-83c3-f490362196d2",
  "rawg_id": 9767,
  "title": "Hollow Knight",
  "cover_url": "https://media.rawg.io/media/games/4cf/...",
  "genre": "Platformer",
  "platform": "PC",
  "release_year": 2017,
  "cached_at": "2026-03-19T21:56:13.015292"
}
```

**Erros**
| Status | Motivo |
|---|---|
| 404 | Jogo não encontrado no banco |
