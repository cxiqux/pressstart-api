# API — Reviews

Endpoints de reviews. Todos requerem autenticação Bearer.

Tag: `Reviews`

---

## GET /games/{game_id}/reviews

Lista todas as reviews públicas de um jogo, ordenadas da mais recente para a mais antiga.

**Response `200`**
```json
[
  {
    "id": "01c4f370-40e3-4af2-9560-d95f09fa3e7e",
    "user_id": "f42acc13-1fb6-4c52-bd7a-25f04aeca789",
    "username": "jogador1",
    "game_id": "9ff5774e-d45b-4f82-83c3-f490362196d2",
    "score": 9,
    "body": "Jogo incrível, atmosfera única.",
    "spoiler": false,
    "created_at": "2026-03-19T22:17:00.324391"
  }
]
```

**Erros**
| Status | Motivo |
|---|---|
| 404 | Jogo não encontrado |

---

## POST /games/{game_id}/reviews

Publica uma review para o jogo. Requer que o jogo tenha status `done` no backlog do usuário.

**Regras de negócio:**
- O jogo deve existir no banco
- O usuário deve ter o jogo no backlog com status `done`
- O usuário só pode ter uma review por jogo

**Body**
```json
{
  "score": 9,
  "body": "Jogo incrível, atmosfera única.",
  "spoiler": false
}
```

**Response `201`**
```json
{
  "id": "01c4f370-40e3-4af2-9560-d95f09fa3e7e",
  "user_id": "f42acc13-1fb6-4c52-bd7a-25f04aeca789",
  "username": "jogador1",
  "game_id": "9ff5774e-d45b-4f82-83c3-f490362196d2",
  "score": 9,
  "body": "Jogo incrível, atmosfera única.",
  "spoiler": false,
  "created_at": "2026-03-19T22:17:00.324391"
}
```

**Erros**
| Status | Motivo |
|---|---|
| 400 | Jogo não encontrado |
| 400 | Jogo não tem status `done` no backlog do usuário |
| 400 | Usuário já avaliou esse jogo |

---

## DELETE /reviews/{review_id}

Remove uma review do usuário autenticado.

**Response `204`** — sem body

**Erros**
| Status | Motivo |
|---|---|
| 403 | A review não pertence ao usuário autenticado |
| 404 | Review não encontrada |
