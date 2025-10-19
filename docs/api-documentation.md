# 🔌 LashManager - Documentação da API

<div align="center">

[![DATAMETRIA](https://img.shields.io/badge/DATAMETRIA-Standards-blue)](https://github.com/datametria/DATAMETRIA-standards)
[![REST API](https://img.shields.io/badge/REST-API-green)](https://restfulapi.net/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-orange)](https://swagger.io/specification/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-red)](https://flask.palletsprojects.com/)

API REST completa para o sistema de gestão de salão de lash designer

[🔐 Autenticação](#-autenticação) • [👥 Clientes](#-clientes) • [📅 Agendamentos](#-agendamentos) • [💰 Pagamentos](#-pagamentos)

</div>

---

## 🌐 Informações Gerais

### 📋 Base URL
```
Desenvolvimento: http://localhost:5000/api
Produção: https://api.lashmanager.com/api
```

### 📊 Versioning
```
Versão atual: v1
Header: Accept: application/vnd.lashmanager.v1+json
```

### 🔒 Autenticação
```
Tipo: Bearer Token (JWT)
Header: Authorization: Bearer <token>
Expiração: 8 horas
```

### 📝 Content-Type
```
Request: application/json
Response: application/json
Charset: UTF-8
```

---

## 🔐 Autenticação

### 🚪 Login

#### `POST /auth/login`

Autentica usuário e retorna token JWT.

**Request Body:**
```json
{
  "username": "admin",
  "password": "senha123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 28800,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@lashmanager.com",
    "role": "admin",
    "funcionario_id": null,
    "ativo": true,
    "last_login": "2025-09-29T10:30:00Z"
  }
}
```

**Response 401:**
```json
{
  "error": "Credenciais inválidas",
  "message": "Username ou password incorretos",
  "code": "INVALID_CREDENTIALS"
}
```

### 🔄 Refresh Token

#### `POST /auth/refresh`

Renova token JWT válido.

**Headers:**
```
Authorization: Bearer <current_token>
```

**Response 200:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires_in": 28800
}
```

### 🚪 Logout

#### `POST /auth/logout`

Invalida token atual.

**Headers:**
```
Authorization: Bearer <token>
```

**Response 200:**
```json
{
  "message": "Logout realizado com sucesso"
}
```

---

## 👥 Clientes

### 📋 Listar Clientes

#### `GET /clientes`

Retorna lista paginada de clientes.

**Query Parameters:**
```
page: int = 1          # Página atual
per_page: int = 20     # Itens por página (max: 100)
search: string         # Busca por nome, telefone ou email
ativo: boolean         # Filtrar por status ativo
order_by: string       # Campo para ordenação (nome, created_at)
order: string          # Direção (asc, desc)
```

**Example Request:**
```
GET /clientes?page=1&per_page=10&search=maria&ativo=true&order_by=nome&order=asc
```

**Response 200:**
```json
{
  "clientes": [
    {
      "id": 1,
      "nome": "Maria Silva",
      "telefone": "(11) 99999-9999",
      "email": "maria@email.com",
      "data_nascimento": "1990-05-15",
      "endereco": "Rua das Flores, 123",
      "observacoes": "Alérgica a cola comum",
      "ativo": true,
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-09-29T14:20:00Z",
      "total_agendamentos": 15,
      "ultimo_agendamento": "2025-09-25T15:00:00Z",
      "valor_total_gasto": 1200.00
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 150,
    "pages": 15,
    "has_prev": false,
    "has_next": true,
    "prev_num": null,
    "next_num": 2
  }
}
```

### 👤 Buscar Cliente

#### `GET /clientes/{id}`

Retorna dados detalhados de um cliente.

**Path Parameters:**
```
id: int (required) - ID do cliente
```

**Response 200:**
```json
{
  "id": 1,
  "nome": "Maria Silva",
  "telefone": "(11) 99999-9999",
  "email": "maria@email.com",
  "data_nascimento": "1990-05-15",
  "endereco": "Rua das Flores, 123",
  "observacoes": "Alérgica a cola comum",
  "ativo": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-09-29T14:20:00Z",
  "estatisticas": {
    "total_agendamentos": 15,
    "agendamentos_concluidos": 13,
    "agendamentos_cancelados": 2,
    "valor_total_gasto": 1200.00,
    "valor_medio_por_sessao": 80.00,
    "ultimo_agendamento": "2025-09-25T15:00:00Z",
    "procedimento_favorito": "Volume Brasileiro"
  },
  "historico_recente": [
    {
      "id": 45,
      "data_hora": "2025-09-25T15:00:00Z",
      "procedimento": "Volume Brasileiro",
      "funcionario": "Ana Costa",
      "valor": 120.00,
      "status": "concluido"
    }
  ]
}
```

**Response 404:**
```json
{
  "error": "Cliente não encontrado",
  "message": "Cliente com ID 999 não existe",
  "code": "CLIENT_NOT_FOUND"
}
```

### ➕ Criar Cliente

#### `POST /clientes`

Cria novo cliente.

**Request Body:**
```json
{
  "nome": "Ana Costa",
  "telefone": "(11) 88888-8888",
  "email": "ana@email.com",
  "data_nascimento": "1985-03-20",
  "endereco": "Av. Paulista, 1000",
  "observacoes": "Prefere horários pela manhã"
}
```

**Response 201:**
```json
{
  "id": 151,
  "nome": "Ana Costa",
  "telefone": "(11) 88888-8888",
  "email": "ana@email.com",
  "data_nascimento": "1985-03-20",
  "endereco": "Av. Paulista, 1000",
  "observacoes": "Prefere horários pela manhã",
  "ativo": true,
  "created_at": "2025-09-29T15:30:00Z",
  "updated_at": "2025-09-29T15:30:00Z"
}
```

**Response 400:**
```json
{
  "error": "Dados inválidos",
  "message": "Erro de validação",
  "code": "VALIDATION_ERROR",
  "details": {
    "nome": ["Campo obrigatório"],
    "telefone": ["Formato inválido. Use (XX) XXXXX-XXXX"],
    "email": ["Email inválido"]
  }
}
```

**Response 409:**
```json
{
  "error": "Cliente já existe",
  "message": "Telefone (11) 88888-8888 já está cadastrado",
  "code": "DUPLICATE_PHONE"
}
```

### ✏️ Atualizar Cliente

#### `PUT /clientes/{id}`

Atualiza dados do cliente.

**Path Parameters:**
```
id: int (required) - ID do cliente
```

**Request Body:**
```json
{
  "nome": "Ana Costa Silva",
  "telefone": "(11) 88888-8888",
  "email": "ana.silva@email.com",
  "data_nascimento": "1985-03-20",
  "endereco": "Av. Paulista, 1000 - Apto 101",
  "observacoes": "Prefere horários pela manhã. Alérgica a níquel."
}
```

**Response 200:**
```json
{
  "id": 151,
  "nome": "Ana Costa Silva",
  "telefone": "(11) 88888-8888",
  "email": "ana.silva@email.com",
  "data_nascimento": "1985-03-20",
  "endereco": "Av. Paulista, 1000 - Apto 101",
  "observacoes": "Prefere horários pela manhã. Alérgica a níquel.",
  "ativo": true,
  "created_at": "2025-09-29T15:30:00Z",
  "updated_at": "2025-09-29T16:45:00Z"
}
```

### 🗑️ Desativar Cliente

#### `DELETE /clientes/{id}`

Desativa cliente (soft delete).

**Path Parameters:**
```
id: int (required) - ID do cliente
```

**Response 200:**
```json
{
  "message": "Cliente desativado com sucesso",
  "id": 151
}
```

---

## 👩💼 Funcionários

### 📋 Listar Funcionários

#### `GET /funcionarios`

Retorna lista de funcionários.

**Query Parameters:**
```
ativo: boolean = true  # Filtrar por status ativo
especialidade: string  # Filtrar por especialidade
```

**Response 200:**
```json
{
  "funcionarios": [
    {
      "id": 1,
      "nome": "Ana Costa",
      "especialidade": "Volume Brasileiro",
      "telefone": "(11) 77777-7777",
      "email": "ana@lashmanager.com",
      "horario_trabalho": {
        "segunda": {"inicio": "08:00", "fim": "17:00"},
        "terca": {"inicio": "08:00", "fim": "17:00"},
        "quarta": {"inicio": "08:00", "fim": "17:00"},
        "quinta": {"inicio": "08:00", "fim": "17:00"},
        "sexta": {"inicio": "08:00", "fim": "17:00"},
        "sabado": {"inicio": "08:00", "fim": "14:00"},
        "domingo": null
      },
      "comissao_percentual": 40.0,
      "ativo": true,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

### 📅 Agenda do Funcionário

#### `GET /funcionarios/{id}/agenda`

Retorna agenda do funcionário.

**Path Parameters:**
```
id: int (required) - ID do funcionário
```

**Query Parameters:**
```
data_inicio: date (required) - Data inicial (YYYY-MM-DD)
data_fim: date (required)    - Data final (YYYY-MM-DD)
```

**Response 200:**
```json
{
  "funcionario": {
    "id": 1,
    "nome": "Ana Costa"
  },
  "periodo": {
    "data_inicio": "2025-09-29",
    "data_fim": "2025-10-05"
  },
  "agendamentos": [
    {
      "id": 45,
      "data_hora": "2025-09-29T09:00:00Z",
      "cliente": {
        "id": 1,
        "nome": "Maria Silva",
        "telefone": "(11) 99999-9999"
      },
      "procedimento": {
        "id": 2,
        "nome": "Volume Brasileiro",
        "duracao_minutos": 150
      },
      "status": "confirmado",
      "observacoes": "Cliente regular"
    }
  ],
  "horarios_livres": [
    {
      "data": "2025-09-29",
      "horarios": ["11:30", "14:00", "16:30"]
    }
  ]
}
```

---

## 🎨 Procedimentos

### 📋 Listar Procedimentos

#### `GET /procedimentos`

Retorna lista de procedimentos disponíveis.

**Query Parameters:**
```
funcionario_id: int    # Filtrar por funcionário
ativo: boolean = true  # Filtrar por status ativo
```

**Response 200:**
```json
{
  "procedimentos": [
    {
      "id": 1,
      "nome": "Extensão Clássica",
      "descricao": "Aplicação fio a fio tradicional",
      "preco": 80.00,
      "duracao_minutos": 120,
      "funcionario": {
        "id": 1,
        "nome": "Ana Costa"
      },
      "ativo": true,
      "created_at": "2025-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "nome": "Volume Brasileiro",
      "descricao": "Técnica de volume com múltiplos fios",
      "preco": 120.00,
      "duracao_minutos": 150,
      "funcionario": {
        "id": 1,
        "nome": "Ana Costa"
      },
      "ativo": true,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

---

## 📅 Agendamentos

### 📋 Listar Agendamentos

#### `GET /agendamentos`

Retorna lista de agendamentos.

**Query Parameters:**
```
data_inicio: date      # Data inicial (YYYY-MM-DD)
data_fim: date         # Data final (YYYY-MM-DD)
cliente_id: int        # Filtrar por cliente
funcionario_id: int    # Filtrar por funcionário
status: string         # Filtrar por status
page: int = 1          # Página atual
per_page: int = 20     # Itens por página
```

**Response 200:**
```json
{
  "agendamentos": [
    {
      "id": 45,
      "data_hora": "2025-09-29T09:00:00Z",
      "cliente": {
        "id": 1,
        "nome": "Maria Silva",
        "telefone": "(11) 99999-9999"
      },
      "funcionario": {
        "id": 1,
        "nome": "Ana Costa"
      },
      "procedimento": {
        "id": 2,
        "nome": "Volume Brasileiro",
        "preco": 120.00,
        "duracao_minutos": 150
      },
      "status": "confirmado",
      "valor_cobrado": 120.00,
      "observacoes": "Cliente regular",
      "created_at": "2025-09-25T10:00:00Z",
      "updated_at": "2025-09-28T14:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 45,
    "pages": 3
  }
}
```

### ➕ Criar Agendamento

#### `POST /agendamentos`

Cria novo agendamento.

**Request Body:**
```json
{
  "cliente_id": 1,
  "funcionario_id": 1,
  "procedimento_id": 2,
  "data_hora": "2025-10-01T14:00:00Z",
  "observacoes": "Primeira vez da cliente"
}
```

**Response 201:**
```json
{
  "id": 46,
  "data_hora": "2025-10-01T14:00:00Z",
  "cliente": {
    "id": 1,
    "nome": "Maria Silva",
    "telefone": "(11) 99999-9999"
  },
  "funcionario": {
    "id": 1,
    "nome": "Ana Costa"
  },
  "procedimento": {
    "id": 2,
    "nome": "Volume Brasileiro",
    "preco": 120.00,
    "duracao_minutos": 150
  },
  "status": "agendado",
  "valor_cobrado": 120.00,
  "observacoes": "Primeira vez da cliente",
  "created_at": "2025-09-29T16:00:00Z",
  "updated_at": "2025-09-29T16:00:00Z"
}
```

**Response 409:**
```json
{
  "error": "Conflito de horário",
  "message": "Funcionário não disponível no horário solicitado",
  "code": "SCHEDULE_CONFLICT",
  "details": {
    "horario_solicitado": "2025-10-01T14:00:00Z",
    "conflito_com": {
      "agendamento_id": 44,
      "cliente": "João Santos",
      "horario": "2025-10-01T13:00:00Z",
      "duracao": 150
    },
    "proximos_horarios_disponiveis": [
      "2025-10-01T16:30:00Z",
      "2025-10-02T09:00:00Z",
      "2025-10-02T11:30:00Z"
    ]
  }
}
```

### ✏️ Atualizar Agendamento

#### `PUT /agendamentos/{id}`

Atualiza agendamento existente.

**Path Parameters:**
```
id: int (required) - ID do agendamento
```

**Request Body:**
```json
{
  "data_hora": "2025-10-01T15:00:00Z",
  "status": "confirmado",
  "observacoes": "Horário reagendado a pedido da cliente"
}
```

**Response 200:**
```json
{
  "id": 46,
  "data_hora": "2025-10-01T15:00:00Z",
  "status": "confirmado",
  "observacoes": "Horário reagendado a pedido da cliente",
  "updated_at": "2025-09-29T16:30:00Z"
}
```

### 🔄 Alterar Status

#### `PATCH /agendamentos/{id}/status`

Altera apenas o status do agendamento.

**Path Parameters:**
```
id: int (required) - ID do agendamento
```

**Request Body:**
```json
{
  "status": "em_andamento"
}
```

**Response 200:**
```json
{
  "id": 46,
  "status": "em_andamento",
  "updated_at": "2025-09-29T17:00:00Z"
}
```

**Status válidos:**
- `agendado` - Agendamento criado
- `confirmado` - Cliente confirmou presença
- `em_andamento` - Procedimento iniciado
- `concluido` - Procedimento finalizado
- `cancelado` - Cancelado pelo cliente/salão
- `nao_compareceu` - Cliente faltou

---

## 💰 Pagamentos

### 📋 Listar Pagamentos

#### `GET /pagamentos`

Retorna lista de pagamentos.

**Query Parameters:**
```
cliente_id: int        # Filtrar por cliente
agendamento_id: int    # Filtrar por agendamento
status: string         # Filtrar por status (pendente, pago, cancelado)
data_inicio: date      # Data inicial
data_fim: date         # Data final
forma_pagamento: string # Filtrar por forma de pagamento
page: int = 1          # Página atual
per_page: int = 20     # Itens por página
```

**Response 200:**
```json
{
  "pagamentos": [
    {
      "id": 23,
      "cliente": {
        "id": 1,
        "nome": "Maria Silva"
      },
      "agendamento": {
        "id": 45,
        "data_hora": "2025-09-29T09:00:00Z",
        "procedimento": "Volume Brasileiro"
      },
      "valor": 120.00,
      "forma_pagamento": "pix",
      "status": "pago",
      "data_vencimento": "2025-09-29",
      "data_pagamento": "2025-09-29T12:30:00Z",
      "observacoes": "Pagamento à vista",
      "created_at": "2025-09-29T09:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 89,
    "pages": 5
  },
  "resumo": {
    "total_pago": 8450.00,
    "total_pendente": 340.00,
    "total_cancelado": 120.00
  }
}
```

### ➕ Registrar Pagamento

#### `POST /pagamentos`

Registra novo pagamento.

**Request Body:**
```json
{
  "cliente_id": 1,
  "agendamento_id": 46,
  "valor": 120.00,
  "forma_pagamento": "cartao_credito",
  "data_pagamento": "2025-09-29T16:00:00Z",
  "observacoes": "Parcelado em 2x"
}
```

**Response 201:**
```json
{
  "id": 24,
  "cliente": {
    "id": 1,
    "nome": "Maria Silva"
  },
  "agendamento": {
    "id": 46,
    "data_hora": "2025-10-01T15:00:00Z",
    "procedimento": "Volume Brasileiro"
  },
  "valor": 120.00,
  "forma_pagamento": "cartao_credito",
  "status": "pago",
  "data_vencimento": "2025-09-29",
  "data_pagamento": "2025-09-29T16:00:00Z",
  "observacoes": "Parcelado em 2x",
  "created_at": "2025-09-29T16:00:00Z"
}
```

**Formas de pagamento válidas:**
- `dinheiro` - Pagamento em espécie
- `pix` - Transferência PIX
- `debito` - Cartão de débito
- `credito` - Cartão de crédito
- `transferencia` - Transferência bancária

---

## 📊 Dashboard e Relatórios

### 📈 Dashboard Principal

#### `GET /dashboard`

Retorna dados do dashboard principal.

**Query Parameters:**
```
data_inicio: date = hoje  # Data inicial para métricas
data_fim: date = hoje     # Data final para métricas
```

**Response 200:**
```json
{
  "resumo_hoje": {
    "agendamentos_total": 8,
    "agendamentos_concluidos": 5,
    "agendamentos_pendentes": 3,
    "receita_realizada": 600.00,
    "receita_prevista": 960.00
  },
  "resumo_mes": {
    "agendamentos_total": 156,
    "agendamentos_concluidos": 142,
    "receita_realizada": 14200.00,
    "receita_prevista": 15600.00,
    "novos_clientes": 12,
    "clientes_retornaram": 89
  },
  "proximos_agendamentos": [
    {
      "id": 47,
      "data_hora": "2025-09-29T18:00:00Z",
      "cliente": "Ana Costa",
      "procedimento": "Manutenção",
      "funcionario": "Maria Santos"
    }
  ],
  "alertas": [
    {
      "tipo": "pagamento_atrasado",
      "mensagem": "3 pagamentos em atraso",
      "prioridade": "alta"
    },
    {
      "tipo": "agendamento_nao_confirmado",
      "mensagem": "5 agendamentos aguardando confirmação",
      "prioridade": "media"
    }
  ]
}
```

### 📊 Relatório Financeiro

#### `GET /relatorios/financeiro`

Retorna relatório financeiro detalhado.

**Query Parameters:**
```
data_inicio: date (required) # Data inicial
data_fim: date (required)    # Data final
funcionario_id: int          # Filtrar por funcionário
procedimento_id: int         # Filtrar por procedimento
```

**Response 200:**
```json
{
  "periodo": {
    "data_inicio": "2025-09-01",
    "data_fim": "2025-09-30"
  },
  "resumo_geral": {
    "receita_total": 14200.00,
    "total_agendamentos": 156,
    "ticket_medio": 91.03,
    "receita_por_forma_pagamento": {
      "pix": 6400.00,
      "dinheiro": 3200.00,
      "cartao_credito": 2800.00,
      "cartao_debito": 1800.00
    }
  },
  "por_funcionario": [
    {
      "funcionario": {
        "id": 1,
        "nome": "Ana Costa"
      },
      "agendamentos": 89,
      "receita": 8900.00,
      "comissao": 3560.00
    }
  ],
  "por_procedimento": [
    {
      "procedimento": {
        "id": 2,
        "nome": "Volume Brasileiro"
      },
      "quantidade": 67,
      "receita": 8040.00,
      "percentual": 56.6
    }
  ]
}
```

---

## 🔍 Busca e Filtros

### 🔎 Busca Global

#### `GET /search`

Busca global no sistema.

**Query Parameters:**
```
q: string (required)   # Termo de busca
tipo: string           # Tipo (clientes, agendamentos, pagamentos)
limit: int = 10        # Limite de resultados
```

**Response 200:**
```json
{
  "query": "maria",
  "resultados": {
    "clientes": [
      {
        "id": 1,
        "nome": "Maria Silva",
        "telefone": "(11) 99999-9999",
        "tipo": "cliente"
      }
    ],
    "agendamentos": [
      {
        "id": 45,
        "cliente": "Maria Silva",
        "data_hora": "2025-09-29T09:00:00Z",
        "tipo": "agendamento"
      }
    ]
  },
  "total_encontrados": 2
}
```

---

## 📱 Notificações

### 📨 Enviar Notificação

#### `POST /notificacoes`

Envia notificação para cliente.

**Request Body:**
```json
{
  "cliente_id": 1,
  "tipo": "lembrete_agendamento",
  "canal": "whatsapp",
  "agendamento_id": 46,
  "mensagem_personalizada": "Olá Maria! Lembrando do seu agendamento amanhã às 14h."
}
```

**Response 201:**
```json
{
  "id": 12,
  "cliente_id": 1,
  "tipo": "lembrete_agendamento",
  "canal": "whatsapp",
  "status": "enviado",
  "enviado_em": "2025-09-29T17:00:00Z"
}
```

---

## ⚠️ Códigos de Erro

### 📋 Códigos HTTP Padrão

| Código | Descrição | Uso |
|--------|-----------|-----|
| `200` | OK | Sucesso |
| `201` | Created | Recurso criado |
| `400` | Bad Request | Dados inválidos |
| `401` | Unauthorized | Token inválido/ausente |
| `403` | Forbidden | Sem permissão |
| `404` | Not Found | Recurso não encontrado |
| `409` | Conflict | Conflito de dados |
| `422` | Unprocessable Entity | Erro de validação |
| `429` | Too Many Requests | Rate limit excedido |
| `500` | Internal Server Error | Erro interno |

### 🔍 Códigos de Erro Customizados

```json
{
  "error": "Título do erro",
  "message": "Descrição detalhada",
  "code": "CODIGO_ERRO",
  "details": {
    "campo": ["Lista de erros específicos"]
  },
  "timestamp": "2025-09-29T17:00:00Z",
  "path": "/api/clientes"
}
```

**Códigos Específicos:**
- `INVALID_CREDENTIALS` - Credenciais inválidas
- `TOKEN_EXPIRED` - Token expirado
- `VALIDATION_ERROR` - Erro de validação
- `DUPLICATE_PHONE` - Telefone duplicado
- `DUPLICATE_EMAIL` - Email duplicado
- `CLIENT_NOT_FOUND` - Cliente não encontrado
- `SCHEDULE_CONFLICT` - Conflito de agendamento
- `INSUFFICIENT_PERMISSIONS` - Permissões insuficientes
- `RATE_LIMIT_EXCEEDED` - Limite de requisições excedido

---

## 🔒 Rate Limiting

### 📊 Limites por Endpoint

| Endpoint | Limite | Janela |
|----------|--------|--------|
| `POST /auth/login` | 5 requests | 1 minuto |
| `GET /clientes` | 100 requests | 1 minuto |
| `POST /clientes` | 20 requests | 1 minuto |
| `POST /agendamentos` | 30 requests | 1 minuto |
| `GET /dashboard` | 60 requests | 1 minuto |
| **Global** | 1000 requests | 1 hora |

### 📋 Headers de Rate Limit

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1696000000
```

---

## 📝 Exemplos de Uso

### 🎯 Fluxo Completo: Novo Agendamento

```javascript
// 1. Login
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'senha123'
  })
});
const { access_token } = await loginResponse.json();

// 2. Buscar cliente
const clienteResponse = await fetch('/api/clientes?search=maria', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const { clientes } = await clienteResponse.json();
const cliente = clientes[0];

// 3. Listar procedimentos
const procedimentosResponse = await fetch('/api/procedimentos', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const { procedimentos } = await procedimentosResponse.json();

// 4. Criar agendamento
const agendamentoResponse = await fetch('/api/agendamentos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    cliente_id: cliente.id,
    funcionario_id: 1,
    procedimento_id: procedimentos[0].id,
    data_hora: '2025-10-01T14:00:00Z'
  })
});
const agendamento = await agendamentoResponse.json();

// 5. Registrar pagamento
const pagamentoResponse = await fetch('/api/pagamentos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    cliente_id: cliente.id,
    agendamento_id: agendamento.id,
    valor: agendamento.valor_cobrado,
    forma_pagamento: 'pix'
  })
});
```

---

## 🧪 Ambiente de Testes

### 🔧 Base URL de Teste
```
https://api-test.lashmanager.com/api
```

### 👤 Usuários de Teste

```json
{
  "admin": {
    "username": "admin_test",
    "password": "test123",
    "role": "admin"
  },
  "funcionario": {
    "username": "funcionario_test",
    "password": "test123",
    "role": "funcionario"
  },
  "recepcionista": {
    "username": "recepcao_test",
    "password": "test123",
    "role": "recepcionista"
  }
}
```

### 📊 Dados de Teste

- **Clientes**: 50 clientes fictícios
- **Agendamentos**: 200 agendamentos (últimos 3 meses)
- **Pagamentos**: 180 pagamentos registrados
- **Reset**: Dados resetados diariamente às 00:00 UTC

---

## 📋 Changelog da API

### v1.0.0 - 2025-09-29
- ✅ Endpoints básicos de CRUD
- ✅ Autenticação JWT
- ✅ Sistema de agendamentos
- ✅ Controle de pagamentos
- ✅ Dashboard e relatórios

### v1.1.0 - Planejado
- 🔄 Notificações WhatsApp
- 🔄 Upload de fotos
- 🔄 Relatórios avançados
- 🔄 Webhooks

---

<div align="center">

**Desenvolvido com 💜 por Lila Rodrigues**

*Documentação completa da API LashManager v1.0*

**Última atualização**: 29/09/2025
**Próxima revisão**: Dezembro 2025

</div>