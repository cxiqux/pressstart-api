# API — Users

Endpoints de perfil de usuário. Todos requerem autenticação Bearer.

Prefix: `/users` | Tag: `Users`

---

## GET /users/me

Retorna o perfil do usuário autenticado.

**Response `200`**
```json
{
  "id": "f42acc13-1fb6-4c52-bd7a-25f04aeca789",
  "username": "caique",
  "email": "caique@pressstart.dev",
  "avatar_url": null,
  "created_at": "2026-03-19T21:55:51.310168"
}
```

---

## PATCH /users/me

Atualiza username e/ou avatar do usuário autenticado. Todos os campos são opcionais.

**Body**
```json
{
  "username": "novo_username",
  "avatar_url": "https://exemplo.com/avatar.jpg"
}
```

**Response `200`** — usuário atualizado (mesmo formato de `GET /users/me`)

**Erros**
| Status | Motivo |
|---|---|
| 400 | Username já em uso por outro usuário |

---

## GET /users/{username}

Retorna o perfil público de um usuário pelo username. Não expõe `email`.

> Requer autenticação mesmo sendo perfil público — pode ser revisado no futuro para acesso anônimo.

**Response `200`**
```json
{
  "id": "f42acc13-1fb6-4c52-bd7a-25f04aeca789",
  "username": "caique",
  "email": "caique@pressstart.dev",
  "avatar_url": null,
  "created_at": "2026-03-19T21:55:51.310168"
}
```

**Erros**
| Status | Motivo |
|---|---|
| 404 | Usuário não encontrado |
