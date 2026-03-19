# API — Backlog

Endpoints do backlog pessoal. Todos requerem autenticação Bearer.

O backlog é sempre do usuário autenticado — não é possível acessar ou modificar o backlog de outro usuário por esses endpoints.

Prefix: `/backlog` | Tag: `Backlog`

---

## GET /backlog

Lista o backlog do usuário autenticado. Suporta filtro por status, ordenação e paginação.

**Query params**

| Param | Tipo | Padrão | Opções |
|---|---|---|---|
| `status` | string | — | `want`, `playing`, `done`, `dropped` |
| `sort` | string | `updated_at` | `updated_at`, `score`, `title` |
| `page` | int | `1` | ≥ 1 |

**Response `200`**
```json
[
  {
    "id": "4300f0db-ea77-47d9-9fbf-ed315fec5701",
    "game_id": "9ff5774e-d45b-4f82-83c3-f490362196d2",
    "game": {
      "id": "9ff5774e-d45b-4f82-83c3-f490362196d2",
      "rawg_id": 9767,
      "title": "Hollow Knight",
      "cover_url": "https://media.rawg.io/...",
      "genre": "Platformer",
      "platform": "PC",
      "release_year": 2017,
      "cached_at": "2026-03-19T21:56:13.015292"
    },
    "status": "done",
    "score": 9,
    "notes": null,
    "hours_played": 40,
    "updated_at": "2026-03-19T22:13:56.324081"
  }
]
```

Page size fixo em 20 itens.

---

## POST /backlog

Adiciona um jogo ao backlog. O jogo é identificado pelo `rawg_id` — se ainda não estiver no cache local, é buscado na RAWG automaticamente.

**Body**
```json
{
  "rawg_id": 9767,
  "status": "playing",
  "score": null,
  "notes": "Comecei hoje",
  "hours_played": 0
}
```

**Response `201`** — entrada criada (mesmo formato de `GET /backlog`)

**Erros**
| Status | Motivo |
|---|---|
| 400 | Jogo não encontrado na RAWG |
| 400 | Jogo já está no backlog |

---

## PATCH /backlog/{entry_id}

Atualiza uma entrada do backlog. Todos os campos são opcionais — só atualiza o que for enviado.

**Body**
```json
{
  "status": "done",
  "score": 9,
  "hours_played": 40,
  "notes": "Platinado"
}
```

**Response `200`** — entrada atualizada

**Erros**
| Status | Motivo |
|---|---|
| 403 | A entrada não pertence ao usuário autenticado |
| 404 | Entrada não encontrada |

---

## DELETE /backlog/{entry_id}

Remove uma entrada do backlog.

**Response `204`** — sem body

**Erros**
| Status | Motivo |
|---|---|
| 403 | A entrada não pertence ao usuário autenticado |
| 404 | Entrada não encontrada |
