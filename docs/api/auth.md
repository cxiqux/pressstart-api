# API — Auth

Endpoints de autenticação. Nenhum requer token.

Prefix: `/auth` | Tag: `Auth`

---

## POST /auth/register

Cria um novo usuário e retorna os tokens de acesso.

**Body**
```json
{
  "username": "caique",
  "email": "caique@pressstart.dev",
  "password": "minhasenha"
}
```

**Response `201`**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Erros**
| Status | Motivo |
|---|---|
| 400 | E-mail já cadastrado |
| 400 | Username já cadastrado |
| 422 | Body inválido (e-mail malformado, campo ausente) |

---

## POST /auth/login

Autentica um usuário existente.

**Body**
```json
{
  "email": "caique@pressstart.dev",
  "password": "minhasenha"
}
```

**Response `200`**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Erros**
| Status | Motivo |
|---|---|
| 401 | Credenciais inválidas (mensagem genérica — não especifica se foi e-mail ou senha) |

---

## POST /auth/refresh

Renova o access token usando um refresh token válido.

**Body**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response `200`**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

> Ambos os tokens são renovados na resposta.

**Erros**
| Status | Motivo |
|---|---|
| 401 | Refresh token inválido ou expirado |
| 401 | Usuário não encontrado |
